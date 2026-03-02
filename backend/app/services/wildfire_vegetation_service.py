"""
USFS Wildfire Hazard Potential (WHP) lookup.

Queries the USFS ArcGIS REST service for the pre-computed Wildfire Hazard
Potential at a given coordinate. WHP incorporates vegetation density, fuel
types, topography, and fire weather into a single score.
"""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger("safehaven.wildfire_veg")

# USFS Wildfire Hazard Potential 2023 MapServer
WHP_URL = (
    "https://apps.fs.usda.gov/arcx/rest/services/"
    "RDW_Wildfire/RMRS_WildfireHazardPotential_2023/MapServer/identify"
)


async def get_wildfire_hazard_potential(
    client: httpx.AsyncClient,
    lat: float,
    lng: float,
) -> dict:
    """
    Return USFS Wildfire Hazard Potential for the given coordinate.

    Returns
    -------
    dict with keys:
        whp_value : int | None  (raw pixel value)
        whp_class : str  ("Very Low" / "Low" / "Moderate" / "High" / "Very High" / "Non-Burnable" / "Unknown")
    """
    params = {
        "geometry": f"{lng},{lat}",
        "geometryType": "esriGeometryPoint",
        "sr": 4326,
        "layers": "all",
        "tolerance": 1,
        "mapExtent": f"{lng - 0.01},{lat - 0.01},{lng + 0.01},{lat + 0.01}",
        "imageDisplay": "800,600,96",
        "returnGeometry": "false",
        "f": "json",
    }

    try:
        resp = await client.get(WHP_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results", [])
        if not results:
            return {"whp_value": None, "whp_class": "Unknown"}

        attrs = results[0].get("attributes", {})
        # The WHP raster has a "Pixel Value" or "gridcode" attribute
        pixel_value = attrs.get("Pixel Value") or attrs.get("gridcode") or attrs.get("GRIDCODE")

        if pixel_value is None or pixel_value == "NoData":
            return {"whp_value": None, "whp_class": "Non-Burnable"}

        pixel_value = int(float(pixel_value))

        # WHP classification (based on USFS documentation)
        # The 2023 WHP uses a continuous scale, classified into 5 categories
        if pixel_value <= 0:
            whp_class = "Non-Burnable"
        elif pixel_value <= 3:
            whp_class = "Very Low"
        elif pixel_value <= 5:
            whp_class = "Low"
        elif pixel_value <= 7:
            whp_class = "Moderate"
        elif pixel_value <= 9:
            whp_class = "High"
        else:
            whp_class = "Very High"

        return {
            "whp_value": pixel_value,
            "whp_class": whp_class,
        }

    except Exception as exc:
        logger.warning("USFS WHP query failed: %s", exc)
        return {"whp_value": None, "whp_class": "Unknown"}
