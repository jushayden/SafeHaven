"""
/api/risk-profile -- Comprehensive natural-hazard risk assessment.

Strategy
--------
1.  Reverse-geocode the provided lat/lng to determine the US state.
2.  Look up curated state-level risk data (the *primary* data source).
3.  In parallel, query the USGS Earthquake Hazards API for recent nearby
    seismic events (this API is free and reliable).
4.  Merge the live earthquake data into the response so the frontend can
    display recent quakes on a map.
5.  If reverse geocoding fails, return a sensible "unknown location" fallback.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Optional

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.config import GOOGLE_MAPS_API_KEY
from app.data.risk_data import get_state_risk, severity_label

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
    earthquake, and wildfire -- plus a list of recent earthquakes from USGS.
    """
    async with httpx.AsyncClient(timeout=15) as client:
        # Run reverse geocode and USGS query in parallel
        geo_task = _reverse_geocode(client, lat, lng)
        eq_task = _fetch_recent_earthquakes(client, lat, lng)
        (state_code, address, state_name), earthquakes = await asyncio.gather(
            geo_task, eq_task
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

        # Recalculate overall risk
        max_score = max(
            risk_info["risks"][h]["score"]
            for h in ("hurricane", "flood", "earthquake", "wildfire")
        )
        risk_info["overall_risk"] = severity_label(max_score)

    return {
        "address": address or f"{lat}, {lng}",
        "state": state_code or "Unknown",
        "state_name": state_name or "Unknown",
        "risks": risk_info["risks"],
        "overall_risk": risk_info["overall_risk"],
        "recent_earthquakes": earthquakes,
    }
