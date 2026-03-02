"""
/api/emergency-contacts -- Return curated emergency contacts for a US state.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, Query

from app.data.emergency_contacts import get_emergency_contacts

logger = logging.getLogger("safehaven.emergency_contacts")
router = APIRouter()


@router.get("/emergency-contacts")
async def emergency_contacts(
    state: str = Query(
        ...,
        min_length=2,
        max_length=2,
        description="Two-letter US state abbreviation (e.g. FL, CA, TX)",
    ),
):
    """
    Return state-level emergency contacts including:

    - 911 and universal numbers
    - State emergency management agency
    - FEMA regional office
    - American Red Cross chapter
    - National Weather Service office
    """
    contacts = get_emergency_contacts(state)

    return {
        "state": state.upper(),
        "contacts": contacts,
    }
