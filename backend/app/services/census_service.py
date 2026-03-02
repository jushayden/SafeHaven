"""
US Census population density lookup.

Uses the Census Bureau's free TIGERweb REST API to get population density
for the census tract containing the given coordinates.
"""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger("safehaven.census")

# TIGERweb ACS 2020 census tracts -- returns population & area for a point
TIGERWEB_URL = (
    "https://tigerweb.geo.census.gov/arcgis/rest/services/"
    "TIGERweb/tigerWMS_ACS2020/MapServer/8/query"
)


async def get_population_density(
    client: httpx.AsyncClient,
    lat: float,
    lng: float,
) -> dict:
    """
    Return population density for the census tract containing the coordinate.

    Returns
    -------
    dict with keys:
        population : int | None
        area_sq_miles : float | None
        density_per_sq_mile : float | None
        density_label : str  ("Very Low" / "Low" / "Moderate" / "High" / "Very High")
    """
    params = {
        "geometry": f"{lng},{lat}",
        "geometryType": "esriGeometryPoint",
        "inSR": 4326,
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "POP100,AREALAND",
        "returnGeometry": "false",
        "f": "json",
    }

    try:
        resp = await client.get(TIGERWEB_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        features = data.get("features", [])
        if not features:
            return _empty()

        attrs = features[0].get("attributes", {})
        population = attrs.get("POP100")
        area_land = attrs.get("AREALAND")  # in square meters

        if population is None or area_land is None or area_land == 0:
            return _empty()

        area_sq_miles = round(area_land / 2_589_988, 2)  # m² to mi²
        density = round(population / area_sq_miles, 1) if area_sq_miles > 0 else 0

        return {
            "population": population,
            "area_sq_miles": area_sq_miles,
            "density_per_sq_mile": density,
            "density_label": _density_label(density),
        }

    except Exception as exc:
        logger.warning("Census population density query failed: %s", exc)
        return _empty()


def _density_label(density: float) -> str:
    if density < 100:
        return "Very Low"
    elif density < 500:
        return "Low"
    elif density < 2000:
        return "Moderate"
    elif density < 10000:
        return "High"
    else:
        return "Very High"


def _empty() -> dict:
    return {
        "population": None,
        "area_sq_miles": None,
        "density_per_sq_mile": None,
        "density_label": "Unknown",
    }
