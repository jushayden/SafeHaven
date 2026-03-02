"""
/api/risk-profile -- Comprehensive natural-hazard risk assessment.

Strategy
--------
1.  Reverse-geocode the provided lat/lng to determine the US state.
2.  Look up curated state-level risk data (the *primary* data source).
3.  In parallel, query:
    - USGS Earthquake Hazards API for recent nearby seismic events
    - USGS Elevation Point Query Service for ground elevation
    - Census Bureau TIGERweb for population density
4.  Calculate proximity to the nearest coastline.
5.  Adjust base risk scores using elevation, coast proximity, and density.
6.  Return the enriched response to the frontend.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Optional

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.config import GOOGLE_MAPS_API_KEY
from app.data.risk_data import get_state_risk, severity_label
from app.services.elevation_service import get_elevation
from app.services.coast_service import get_coast_proximity
from app.services.census_service import get_population_density
from app.services.building_age_service import get_building_age
from app.services.wildfire_vegetation_service import get_wildfire_hazard_potential

logger = logging.getLogger("safehaven.risk_profile")
router = APIRouter()

GOOGLE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"
USGS_EARTHQUAKE_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _reverse_geocode(
    client: httpx.AsyncClient,
    lat: float,
    lng: float,
) -> tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Reverse-geocode (lat, lng) to (state_code, formatted_address, state_name).
    Returns (None, None, None) when the API key is missing or the call fails.
    """
    if not GOOGLE_MAPS_API_KEY:
        return None, None, None

    params = {"latlng": f"{lat},{lng}", "key": GOOGLE_MAPS_API_KEY}
    try:
        resp = await client.get(GOOGLE_GEOCODE_URL, params=params)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        logger.warning("Reverse geocode failed: %s", exc)
        return None, None, None

    if data.get("status") != "OK" or not data.get("results"):
        return None, None, None

    formatted_address = data["results"][0].get("formatted_address", "")
    state_code: Optional[str] = None
    state_name: Optional[str] = None

    for result in data["results"]:
        for component in result.get("address_components", []):
            if "administrative_area_level_1" in component.get("types", []):
                state_code = component.get("short_name")
                state_name = component.get("long_name")
                break
        if state_code:
            break

    return state_code, formatted_address, state_name


async def _fetch_recent_earthquakes(
    client: httpx.AsyncClient,
    lat: float,
    lng: float,
    radius_km: int = 250,
    limit: int = 10,
) -> List[Dict[str, Any]]:
    """
    Query the USGS Earthquake Hazards API for recent earthquakes within
    *radius_km* of the given point.  Returns at most *limit* events sorted
    by time descending.
    """
    params = {
        "format": "geojson",
        "latitude": lat,
        "longitude": lng,
        "maxradiuskm": radius_km,
        "orderby": "time",
        "limit": limit,
        "minmagnitude": 2.5,
    }

    try:
        resp = await client.get(USGS_EARTHQUAKE_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        logger.warning("USGS earthquake query failed: %s", exc)
        return []

    earthquakes: List[Dict[str, Any]] = []
    for feature in data.get("features", []):
        props = feature.get("properties", {})
        coords = feature.get("geometry", {}).get("coordinates", [None, None, None])
        earthquakes.append({
            "magnitude": props.get("mag"),
            "place": props.get("place"),
            "time": props.get("time"),
            "url": props.get("url"),
            "lat": coords[1] if len(coords) > 1 else None,
            "lng": coords[0] if len(coords) > 0 else None,
            "depth_km": coords[2] if len(coords) > 2 else None,
        })

    return earthquakes


def _adjust_earthquake_score(
    base_score: int,
    earthquakes: List[Dict[str, Any]],
) -> int:
    """
    Optionally boost the earthquake score when the USGS data shows notable
    recent activity near the location.
    """
    if not earthquakes:
        return base_score

    max_mag = max((eq.get("magnitude") or 0) for eq in earthquakes)
    count = len(earthquakes)

    bonus = 0
    if max_mag >= 6.0:
        bonus += 15
    elif max_mag >= 5.0:
        bonus += 10
    elif max_mag >= 4.0:
        bonus += 5

    if count >= 8:
        bonus += 5
    elif count >= 4:
        bonus += 3

    return min(100, base_score + bonus)


def _adjust_scores_with_location_data(
    risk_info: Dict[str, Any],
    elevation: Dict[str, Any],
    coast: Dict[str, Any],
    density: Dict[str, Any],
    **kwargs,
) -> None:
    """
    Adjust base risk scores using elevation, coast proximity, and density.
    Modifies risk_info in place.
    """
    risks = risk_info["risks"]

    # --- Elevation adjustments (flood risk) ---
    elev_ft = elevation.get("elevation_ft")
    if elev_ft is not None:
        flood = risks["flood"]
        if elev_ft <= 10:
            flood["score"] = min(100, flood["score"] + 15)
        elif elev_ft <= 30:
            flood["score"] = min(100, flood["score"] + 10)
        elif elev_ft <= 50:
            flood["score"] = min(100, flood["score"] + 5)
        elif elev_ft >= 500:
            flood["score"] = max(0, flood["score"] - 10)
        elif elev_ft >= 200:
            flood["score"] = max(0, flood["score"] - 5)
        flood["severity"] = severity_label(flood["score"])

    # --- Coast proximity adjustments (hurricane & flood) ---
    coast_dist = coast.get("coast_distance_miles")
    if coast_dist is not None:
        hurricane = risks["hurricane"]
        flood = risks["flood"]

        if coast_dist <= 10:
            hurricane["score"] = min(100, hurricane["score"] + 12)
            flood["score"] = min(100, flood["score"] + 8)
        elif coast_dist <= 30:
            hurricane["score"] = min(100, hurricane["score"] + 8)
            flood["score"] = min(100, flood["score"] + 4)
        elif coast_dist <= 50:
            hurricane["score"] = min(100, hurricane["score"] + 4)
        elif coast_dist >= 200:
            hurricane["score"] = max(0, hurricane["score"] - 8)
        elif coast_dist >= 100:
            hurricane["score"] = max(0, hurricane["score"] - 4)

        hurricane["severity"] = severity_label(hurricane["score"])
        flood["severity"] = severity_label(flood["score"])

    # --- Population density adjustments ---
    density_val = density.get("density_per_sq_mile")
    if density_val is not None:
        # High density = harder evacuations, more infrastructure strain
        # Slightly increase all risk scores for very high density
        if density_val >= 10000:
            for key in risks:
                risks[key]["score"] = min(100, risks[key]["score"] + 3)
                risks[key]["severity"] = severity_label(risks[key]["score"])

    # --- Building age adjustments (earthquake & hurricane) ---
    building_age = kwargs.get("building_age", {})
    pct_pre_1980 = building_age.get("pct_pre_1980")
    if pct_pre_1980 is not None:
        eq = risks["earthquake"]
        hur = risks["hurricane"]
        if pct_pre_1980 >= 70:
            eq["score"] = min(100, eq["score"] + 12)
            hur["score"] = min(100, hur["score"] + 8)
        elif pct_pre_1980 >= 50:
            eq["score"] = min(100, eq["score"] + 8)
            hur["score"] = min(100, hur["score"] + 5)
        elif pct_pre_1980 >= 30:
            eq["score"] = min(100, eq["score"] + 4)
            hur["score"] = min(100, hur["score"] + 3)
        # Newer buildings are more resilient
        elif pct_pre_1980 <= 10:
            eq["score"] = max(0, eq["score"] - 5)
            hur["score"] = max(0, hur["score"] - 3)
        eq["severity"] = severity_label(eq["score"])
        hur["severity"] = severity_label(hur["score"])

    # --- Wildfire vegetation adjustments ---
    whp = kwargs.get("wildfire_vegetation", {})
    whp_value = whp.get("whp_value")
    if whp_value is not None:
        wf = risks["wildfire"]
        if whp_value >= 10:     # Very High
            wf["score"] = min(100, wf["score"] + 15)
        elif whp_value >= 8:    # High
            wf["score"] = min(100, wf["score"] + 10)
        elif whp_value >= 6:    # Moderate
            wf["score"] = min(100, wf["score"] + 5)
        elif whp_value <= 0:    # Non-Burnable
            wf["score"] = max(0, wf["score"] - 10)
        elif whp_value <= 3:    # Very Low
            wf["score"] = max(0, wf["score"] - 5)
        wf["severity"] = severity_label(wf["score"])

    # Recalculate overall risk
    max_score = max(risks[h]["score"] for h in ("hurricane", "flood", "earthquake", "wildfire"))
    risk_info["overall_risk"] = severity_label(max_score)


# ---------------------------------------------------------------------------
# Route
# ---------------------------------------------------------------------------

@router.get("/risk-profile")
async def risk_profile(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
):
    """
    Compute a comprehensive natural-hazard risk profile for a location.

    The response contains risk scores and severity labels for hurricane, flood,
    earthquake, and wildfire -- plus elevation, coast proximity, population
    density, and recent earthquakes.
    """
    # Coast proximity is a pure calculation (no network), run immediately
    coast = get_coast_proximity(lat, lng)

    async with httpx.AsyncClient(timeout=15) as client:
        # Run all async queries in parallel
        geo_task = _reverse_geocode(client, lat, lng)
        eq_task = _fetch_recent_earthquakes(client, lat, lng)
        elev_task = get_elevation(client, lat, lng)
        density_task = get_population_density(client, lat, lng)
        building_task = get_building_age(client, lat, lng)
        whp_task = get_wildfire_hazard_potential(client, lat, lng)

        (state_code, address, state_name), earthquakes, elevation, density, building_age, wildfire_veg = (
            await asyncio.gather(geo_task, eq_task, elev_task, density_task, building_task, whp_task)
        )

    # Determine state-level risk data
    risk_info: Optional[Dict[str, Any]] = None
    if state_code:
        risk_info = get_state_risk(state_code)

    if risk_info is None:
        # Unknown state -- return a neutral baseline so the API never 404s
        risk_info = {
            "risks": {
                "hurricane": {"score": 25, "severity": "Moderate", "description": "Risk data unavailable for this location. Moderate baseline assumed."},
                "flood": {"score": 25, "severity": "Moderate", "description": "Risk data unavailable for this location. Moderate baseline assumed."},
                "earthquake": {"score": 25, "severity": "Moderate", "description": "Risk data unavailable for this location. Moderate baseline assumed."},
                "wildfire": {"score": 25, "severity": "Moderate", "description": "Risk data unavailable for this location. Moderate baseline assumed."},
            },
            "overall_risk": "Moderate",
        }

    # Enhance earthquake score with live USGS data
    eq_risk = risk_info["risks"]["earthquake"]
    adjusted_score = _adjust_earthquake_score(eq_risk["score"], earthquakes)
    if adjusted_score != eq_risk["score"]:
        eq_risk["score"] = adjusted_score
        eq_risk["severity"] = severity_label(adjusted_score)

    # Adjust scores with location-specific data
    _adjust_scores_with_location_data(
        risk_info, elevation, coast, density,
        building_age=building_age,
        wildfire_vegetation=wildfire_veg,
    )

    return {
        "address": address or f"{lat}, {lng}",
        "state": state_code or "Unknown",
        "state_name": state_name or "Unknown",
        "risks": risk_info["risks"],
        "overall_risk": risk_info["overall_risk"],
        "recent_earthquakes": earthquakes,
        "location_factors": {
            "elevation": elevation,
            "coast_proximity": coast,
            "population_density": density,
            "building_age": building_age,
            "wildfire_vegetation": wildfire_veg,
        },
    }
