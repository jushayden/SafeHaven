"""
/api/shelters -- Find nearby shelters, hospitals, and fire stations via
the Google Places API (Nearby Search).
"""

from __future__ import annotations

import asyncio
import logging
import math
from typing import Any, Dict, List

import httpx
from fastapi import APIRouter, HTTPException, Query

from app.config import GOOGLE_MAPS_API_KEY

logger = logging.getLogger("safehaven.shelters")
router = APIRouter()

GOOGLE_PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

# Place types we care about, plus a human-readable label for each
PLACE_CATEGORIES: List[Dict[str, str]] = [
    {"type": "hospital", "label": "Hospital"},
    {"type": "fire_station", "label": "Fire Station"},
    {"type": "police", "label": "Police Station"},
    {"type": "local_government_office", "label": "Government Office / Shelter"},
    {"type": "church", "label": "Place of Worship / Potential Shelter"},
]


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return the great-circle distance in kilometres between two points."""
    R = 6371.0  # Earth radius in km
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


async def _search_places(
    client: httpx.AsyncClient,
    lat: float,
    lng: float,
    place_type: str,
    label: str,
    radius: int,
) -> List[Dict[str, Any]]:
    """Query Google Places Nearby Search for a single *place_type*."""
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": place_type,
        "key": GOOGLE_MAPS_API_KEY,
    }

    try:
        resp = await client.get(GOOGLE_PLACES_URL, params=params)
        resp.raise_for_status()
        data = resp.json()
    except Exception as exc:
        logger.warning("Places API error for type=%s: %s", place_type, exc)
        return []

    if data.get("status") not in ("OK", "ZERO_RESULTS"):
        logger.warning("Places API status=%s for type=%s", data.get("status"), place_type)
        return []

    results: List[Dict[str, Any]] = []
    for place in data.get("results", [])[:5]:  # cap per category
        loc = place.get("geometry", {}).get("location", {})
        p_lat = loc.get("lat", 0)
        p_lng = loc.get("lng", 0)
        dist = _haversine_km(lat, lng, p_lat, p_lng)

        results.append({
            "name": place.get("name", "Unknown"),
            "address": place.get("vicinity", ""),
            "lat": p_lat,
            "lng": p_lng,
            "type": label,
            "place_type": place_type,
            "distance_km": round(dist, 2),
            "rating": place.get("rating"),
            "open_now": place.get("opening_hours", {}).get("open_now"),
        })

    return results


@router.get("/shelters")
async def shelters(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
    radius: int = Query(10000, description="Search radius in metres (default 10 km)"),
):
    """
    Find nearby shelters, hospitals, fire stations, and other emergency
    resources within *radius* metres of the given coordinates.
    """
    if not GOOGLE_MAPS_API_KEY:
        raise HTTPException(status_code=503, detail="Google Maps API key is not configured.")

    async with httpx.AsyncClient(timeout=15) as client:
        tasks = [
            _search_places(client, lat, lng, cat["type"], cat["label"], radius)
            for cat in PLACE_CATEGORIES
        ]
        batches = await asyncio.gather(*tasks)

    # Flatten and sort by distance
    all_places: List[Dict[str, Any]] = []
    for batch in batches:
        all_places.extend(batch)
    all_places.sort(key=lambda p: p["distance_km"])

    return {
        "lat": lat,
        "lng": lng,
        "radius_m": radius,
        "count": len(all_places),
        "places": all_places,
    }
