"""
/api/historical-disasters -- Fetch FEMA disaster declarations for a state.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List

import httpx
from fastapi import APIRouter, Query

logger = logging.getLogger("safehaven.historical_disasters")
router = APIRouter()

FEMA_API_URL = "https://www.fema.gov/api/open/v2/DisasterDeclarationsSummaries"


@router.get("/historical-disasters")
async def historical_disasters(
    state: str = Query(..., description="Two-letter state code (e.g. FL)"),
    limit: int = Query(50, description="Max results"),
):
    """
    Fetch historical FEMA disaster declarations for a state.
    The FEMA API is public and requires no key.
    """
    upper_state = state.upper()
    top = min(limit * 10, 1000)  # Request more since FEMA returns per-county rows

    params = {
        "$filter": f"state eq '{upper_state}'",
        "$orderby": "declarationDate desc",
        "$top": str(top),
        "$select": "disasterNumber,declarationDate,declarationTitle,incidentType,state,incidentBeginDate,incidentEndDate",
    }

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(FEMA_API_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
    except Exception as exc:
        logger.warning("FEMA API error: %s", exc)
        return {"disasters": [], "count": 0, "state": upper_state}

    raw = data.get("DisasterDeclarationsSummaries", [])

    # Deduplicate by disaster number (multiple entries per county)
    seen = set()
    disasters: List[Dict[str, Any]] = []
    for d in raw:
        num = d.get("disasterNumber")
        if num in seen:
            continue
        seen.add(num)
        disasters.append({
            "disaster_number": num,
            "title": d.get("declarationTitle", "Unknown"),
            "type": d.get("incidentType", "Unknown"),
            "declaration_date": d.get("declarationDate", ""),
            "begin_date": d.get("incidentBeginDate", ""),
            "end_date": d.get("incidentEndDate", ""),
        })

    disasters = disasters[:min(limit, 100)]

    return {
        "disasters": disasters,
        "count": len(disasters),
        "state": upper_state,
    }
