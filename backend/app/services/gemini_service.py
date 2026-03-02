"""
Wrapper around the Google Generative AI (Gemini) SDK.

Provides a single public function -- ``generate_safety_report`` -- that takes
structured risk-profile data and returns a comprehensive, human-readable
disaster-preparedness report.

If the Gemini API is unavailable or the API key is missing, a deterministic
template-based fallback report is returned so the user always gets *something*
useful.
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from app.config import GEMINI_API_KEY

logger = logging.getLogger("safehaven.gemini")

# ---------------------------------------------------------------------------
# SDK setup
# ---------------------------------------------------------------------------
_client = None


def _get_client():
    """Get or create the GenAI client."""
    global _client
    if _client is not None:
        return _client
    if not GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY is not set -- AI reports will use the fallback template.")
        return None
    from google import genai
    _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


# ---------------------------------------------------------------------------
# Prompt engineering
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """\
You are SafeHaven AI, an expert disaster-preparedness advisor.  Your goal is
to help people understand the natural-hazard risks in their area and take
concrete steps to protect themselves and their families.

Your tone is calm, authoritative, and empathetic -- never alarmist, but always
honest about genuine risks.  When suggesting actions, be specific: name
products, quantities, timeframes, and local resources whenever possible.
"""

def _build_user_prompt(risk_data: Dict[str, Any]) -> str:
    """Build the user-facing prompt from structured risk data."""
    address = risk_data.get("address", "the specified location")
    state = risk_data.get("state", "N/A")
    risks = risk_data.get("risks", {})
    overall = risk_data.get("overall_risk", "Unknown")

    risk_lines: list[str] = []
    for hazard_name in ("hurricane", "flood", "earthquake", "wildfire"):
        info = risks.get(hazard_name, {})
        score = info.get("score", "N/A")
        severity = info.get("severity", "Unknown")
        desc = info.get("description", "")
        risk_lines.append(f"- **{hazard_name.title()}**: Score {score}/100 ({severity}) -- {desc}")

    risk_block = "\n".join(risk_lines)

    return f"""\
Generate a comprehensive disaster-preparedness report for the following location.

**Location:** {address} (State: {state})
**Overall risk level:** {overall}

**Individual hazard assessments:**
{risk_block}

**Important context:** These risk scores are regional estimates based on state and
county-level data from FEMA, USGS, and NOAA. They do not reflect property-specific
factors such as elevation, building construction, local drainage, or proximity to
water bodies. Mention this caveat briefly in the summary and encourage the reader
to consult local floodplain maps and their county emergency management office for
site-specific assessments.

Please structure your report with the following sections (use Markdown headings):

## 1. Overall Risk Assessment Summary
Provide a 2-3 paragraph summary interpreting the risk scores above in plain
language.  Mention which hazards are most urgent and why.

## 2. Top 3 Recommended Preparedness Actions
List the three most impactful things a resident at this address should do
*right now* to improve their safety, ranked by urgency.

## 3. Historical Disaster Context
Briefly describe 2-3 notable historical disasters that have affected this
state or region, including approximate dates and impacts.

## 4. Personalized Emergency Supply Checklist
Provide a detailed, bulleted checklist of supplies tailored to the specific
hazards at this location.  Include quantities for a household of four for
72 hours.

Keep the total report between 600 and 1000 words.
"""


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

async def generate_safety_report(risk_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate an AI-powered safety report for the given risk profile.

    Parameters
    ----------
    risk_data : dict
        A risk-profile payload (as returned by the ``/api/risk-profile``
        endpoint).

    Returns
    -------
    dict
        ``{"report": "<markdown text>", "source": "gemini" | "fallback"}``
    """
    client = _get_client()
    if client is not None:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=_build_user_prompt(risk_data),
                config={
                    "system_instruction": SYSTEM_PROMPT,
                    "max_output_tokens": 2048,
                },
            )
            return {"report": response.text, "source": "gemini"}
        except Exception as exc:
            logger.error("Gemini API call failed: %s", exc)

    # ---- fallback template ------------------------------------------------
    return {"report": _fallback_report(risk_data), "source": "fallback"}


# ---------------------------------------------------------------------------
# Deterministic fallback
# ---------------------------------------------------------------------------

def _fallback_report(risk_data: Dict[str, Any]) -> str:
    """Return a useful template-based report when Gemini is unavailable."""
    address = risk_data.get("address", "your location")
    state = risk_data.get("state", "your state")
    overall = risk_data.get("overall_risk", "Unknown")
    risks = risk_data.get("risks", {})

    # Sort hazards by score descending
    sorted_hazards = sorted(
        risks.items(),
        key=lambda item: item[1].get("score", 0),
        reverse=True,
    )

    hazard_summaries = ""
    for name, info in sorted_hazards:
        hazard_summaries += (
            f"- **{name.title()}** -- Severity: {info.get('severity', 'N/A')} "
            f"(Score: {info.get('score', 'N/A')}/100). "
            f"{info.get('description', '')}\n"
        )

    top_hazard = sorted_hazards[0][0].title() if sorted_hazards else "Natural disaster"

    checklist_items = [
        "Water -- 1 gallon per person per day for 3 days (12 gallons total for a family of 4)",
        "Non-perishable food -- 3-day supply (canned goods, energy bars, dried fruit)",
        "Battery-powered or hand-crank radio (NOAA Weather Radio)",
        "Flashlight and extra batteries",
        "First aid kit",
        "Whistle (to signal for help)",
        "Dust masks, plastic sheeting, and duct tape for sheltering in place",
        "Moist towelettes, garbage bags, and plastic ties for sanitation",
        "Wrench or pliers to turn off utilities",
        "Manual can opener",
        "Local maps",
        "Cell phone with chargers and a backup battery",
        "Prescription medications (7-day supply)",
        "Important family documents in a waterproof container",
        "Cash in small denominations",
    ]

    # Add hazard-specific items
    if risks.get("hurricane", {}).get("score", 0) >= 50:
        checklist_items.extend([
            "Hurricane shutters or pre-cut plywood for windows",
            "Waterproof tarps and rope",
            "Extra fuel for vehicles (keep tanks full during hurricane season)",
        ])
    if risks.get("earthquake", {}).get("score", 0) >= 50:
        checklist_items.extend([
            "Furniture anchoring straps for bookshelves and heavy furniture",
            "Sturdy shoes near each bed (to walk over broken glass)",
            "Fire extinguisher (earthquakes often cause gas leaks and fires)",
        ])
    if risks.get("wildfire", {}).get("score", 0) >= 50:
        checklist_items.extend([
            "N95 respirator masks for smoke",
            "Go-bag pre-packed near the front door",
            "Copies of homeowner's insurance and photo inventory of belongings",
        ])
    if risks.get("flood", {}).get("score", 0) >= 50:
        checklist_items.extend([
            "Sandbags (or know where to get them from your county)",
            "Waterproof document bag",
            "Sump pump or backup power for existing sump pump",
        ])

    checklist_md = "\n".join(f"- {item}" for item in checklist_items)

    return f"""\
## 1. Overall Risk Assessment Summary

Based on our analysis, **{address}** in **{state}** has an overall disaster risk level
of **{overall}**.  Here is a breakdown of the individual hazard assessments:

{hazard_summaries}

The most significant threat to your area is **{top_hazard}**.  We recommend
prioritizing preparedness measures for this hazard while also maintaining
general readiness for all natural disasters.

## 2. Top 3 Recommended Preparedness Actions

1. **Create a family emergency plan.** Identify meeting points, out-of-area
   contacts, and evacuation routes.  Practice the plan with all household
   members at least twice a year.

2. **Build a 72-hour emergency kit** (see the checklist below).  Store it in
   an easily accessible location and check expiration dates every six months.

3. **Sign up for local alerts.** Register for your county's emergency
   notification system and download the FEMA app for real-time alerts.

## 3. Historical Disaster Context

{state} has a documented history of significant natural disasters.  Residents
are encouraged to review FEMA's disaster declaration history for their state at
https://www.fema.gov/disaster/declarations and to learn from past events to
strengthen personal and community preparedness.

## 4. Personalized Emergency Supply Checklist

{checklist_md}

---
*This report was generated by SafeHaven's template engine.  For a more detailed,
AI-personalized report, ensure the Gemini API key is configured.*
"""
