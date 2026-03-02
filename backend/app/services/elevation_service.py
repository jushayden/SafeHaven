"""
USGS Elevation Point Query Service.

Fetches ground-level elevation for a lat/lng coordinate from the free
USGS National Map Elevation Point Query Service (EPQS).
"""

from __future__ import annotations

import logging

import httpx

logger = logging.getLogger("safehaven.elevation")

USGS_EPQS_URL = "https://epqs.nationalmap.gov/v1/json"


async def get_elevation(
    client: httpx.AsyncClient,
    lat: float,
    lng: float,
) -> dict:
    """
    Return elevation data for the given coordinate.

    Returns
    -------
    dict with keys:
        elevation_ft : float | None
        elevation_m  : float | None
    """
    params = {
        "x": lng,
        "y": lat,
        "units": "Feet",
        "wkid": 4326,
        "includeDate": False,
    }

    try:
        resp = await client.get(USGS_EPQS_URL, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        elevation_ft = data.get("value")
        if elevation_ft is not None:
            elevation_ft = round(float(elevation_ft), 1)
            elevation_m = round(elevation_ft * 0.3048, 1)
        else:
            elevation_ft = None
            elevation_m = None

        return {
            "elevation_ft": elevation_ft,
            "elevation_m": elevation_m,
        }
    except Exception as exc:
        logger.warning("USGS elevation query failed: %s", exc)
        return {"elevation_ft": None, "elevation_m": None}
