"""
/api/noaa-alerts -- Fetch active weather alerts from NOAA for a location.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

import httpx
from fastapi import APIRouter, Query

logger = logging.getLogger("safehaven.noaa_alerts")
router = APIRouter()

NOAA_ALERTS_URL = "https://api.weather.gov/alerts/active"


@router.get("/noaa-alerts")
async def noaa_alerts(
    lat: float = Query(..., description="Latitude"),
    lng: float = Query(..., description="Longitude"),
):
    """
    Fetch active NOAA weather alerts for a given location.
    Uses the weather.gov API which is free and requires no API key.
    """
    headers = {
        "User-Agent": "SafeHaven/1.0 (disaster-resilience-tool)",
        "Accept": "application/geo+json",
    }

    params = {"point": f"{lat},{lng}", "status": "actual", "limit": 20}

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(NOAA_ALERTS_URL, params=params, headers=headers)
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        logger.warning("NOAA API error: %s", exc)
        return {"alerts": [], "count": 0}

    alerts: List[Dict[str, Any]] = []
    for feature in data.get("features", []):
        props = feature.get("properties", {})
        alerts.append({
            "event": props.get("event", "Unknown"),
            "severity": props.get("severity", "Unknown"),
            "urgency": props.get("urgency", "Unknown"),
            "headline": props.get("headline", ""),
            "description": props.get("description", ""),
            "instruction": props.get("instruction", ""),
            "areas": props.get("areaDesc", ""),
            "onset": props.get("onset"),
            "expires": props.get("expires"),
            "sender": props.get("senderName", ""),
        })

    return {"alerts": alerts, "count": len(alerts)}
