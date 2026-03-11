"""
/api/ai-report -- Generate an AI-powered disaster-preparedness report via
Google Gemini, with a template-based fallback.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.services.gemini_service import generate_safety_report

logger = logging.getLogger("safehaven.ai_report")
limiter = Limiter(key_func=get_remote_address)
router = APIRouter()


# ---------------------------------------------------------------------------
# Request model
# ---------------------------------------------------------------------------

class RiskInfo(BaseModel):
    score: int = 0
    severity: str = "Low"
    description: str = ""


class AIReportRequest(BaseModel):
    """Payload accepted by POST /api/ai-report."""
    address: Optional[str] = ""
    state: Optional[str] = ""
    risks: Optional[Dict[str, RiskInfo]] = Field(default_factory=dict)
    overall_risk: Optional[str] = "Unknown"
    # The caller may also send extra fields (e.g. recent_earthquakes); we
    # simply ignore them at validation time but forward everything to Gemini.


# ---------------------------------------------------------------------------
# Route
# ---------------------------------------------------------------------------

@router.post("/ai-report")
@limiter.limit("5/minute")
async def ai_report(request: Request, payload: AIReportRequest):
    """
    Generate a comprehensive disaster-preparedness report.

    Accepts the same shape of data returned by ``GET /api/risk-profile`` and
    sends it to Google Gemini for analysis.  If Gemini is unavailable, a
    deterministic template-based report is returned instead.
    """
    try:
        # Convert Pydantic models to plain dicts for the service layer
        risk_data: Dict[str, Any] = payload.model_dump()

        result = await generate_safety_report(risk_data)

        return {
            "report": result["report"],
            "source": result["source"],
        }
    except Exception as exc:
        logger.error("AI report generation failed: %s", exc)
        raise HTTPException(
            status_code=500,
            detail="Failed to generate AI report. Please try again later.",
        ) from exc
