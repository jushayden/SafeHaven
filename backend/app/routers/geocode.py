"""
/api/geocode -- Forward geocoding via Google Maps Geocoding API.
"""

from __future__ import annotations

import logging

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.config import GOOGLE_MAPS_API_KEY

logger = logging.getLogger("safehaven.geocode")
router = APIRouter()

GOOGLE_GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


@router.get("/geocode")
async def geocode(address: str = Query(..., description="Street address or place name to geocode")):
    """
    Geocode an address string into latitude / longitude coordinates.

    Returns ``{ lat, lng, formatted_address }``.
    """
    if not GOOGLE_MAPS_API_KEY:
        raise HTTPException(status_code=503, detail="Google Maps API key is not configured.")

    params = {"address": address, "key": GOOGLE_MAPS_API_KEY}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(GOOGLE_GEOCODE_URL, params=params)
            response.raise_for_status()
            data = response.json()
    except httpx.HTTPError as exc:
        logger.error("Google Geocoding API request failed: %s", exc)
        raise HTTPException(status_code=502, detail="Failed to reach Google Geocoding API.") from exc

    if data.get("status") != "OK" or not data.get("results"):
        raise HTTPException(
            status_code=404,
            detail=f"Geocoding failed for '{address}'. Google API status: {data.get('status')}",
        )

    result = data["results"][0]
    location = result["geometry"]["location"]

    return {
        "lat": location["lat"],
        "lng": location["lng"],
        "formatted_address": result.get("formatted_address", address),
    }
