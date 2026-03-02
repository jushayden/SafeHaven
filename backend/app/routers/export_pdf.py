"""
/api/export-pdf -- Generate a branded PDF report from risk-profile and AI data.
"""

from __future__ import annotations

import io
import logging
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from fpdf import FPDF
from pydantic import BaseModel, Field

logger = logging.getLogger("safehaven.export_pdf")
router = APIRouter()


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

class RiskDetail(BaseModel):
    score: int = 0
    severity: str = "Low"
    description: str = ""


class EarthquakeInfo(BaseModel):
    magnitude: Optional[float] = None
    place: Optional[str] = None
    time: Optional[int] = None


class PDFExportRequest(BaseModel):
    address: Optional[str] = ""
    state: Optional[str] = ""
    risks: Optional[Dict[str, RiskDetail]] = Field(default_factory=dict)
    overall_risk: Optional[str] = "Unknown"
    recent_earthquakes: Optional[List[EarthquakeInfo]] = Field(default_factory=list)
    report: Optional[str] = ""


# ---------------------------------------------------------------------------
# Colour helpers
# ---------------------------------------------------------------------------

_SEVERITY_COLOURS: Dict[str, tuple] = {
    "Low": (46, 204, 113),       # green
    "Moderate": (241, 196, 15),  # yellow
    "High": (230, 126, 34),      # orange
    "Extreme": (231, 76, 60),    # red
}


def _severity_rgb(severity: str) -> tuple:
    return _SEVERITY_COLOURS.get(severity, (149, 165, 166))


# ---------------------------------------------------------------------------
# PDF generation
# ---------------------------------------------------------------------------

class SafeHavenPDF(FPDF):
    """Custom FPDF subclass with SafeHaven branding."""

    def header(self):
        self.set_font("Helvetica", "B", 18)
        self.set_text_color(41, 128, 185)
        self.cell(0, 10, "SafeHaven", new_x="LMARGIN", new_y="NEXT", align="L")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(127, 140, 141)
        self.cell(0, 5, "AI-Powered Disaster Resilience Report", new_x="LMARGIN", new_y="NEXT", align="L")
        self.line(10, self.get_y() + 2, 200, self.get_y() + 2)
        self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(149, 165, 166)
        self.cell(0, 10, f"SafeHaven Report  |  Page {self.page_no()}/{{nb}}", align="C")

    # -- convenience methods --------------------------------------------------

    def section_title(self, title: str):
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(44, 62, 80)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def body_text(self, text: str):
        self.set_font("Helvetica", "", 10)
        self.set_text_color(52, 73, 94)
        self.multi_cell(0, 5, text)
        self.ln(2)

    def risk_badge(self, label: str, score: int, severity: str, description: str):
        r, g, b = _severity_rgb(severity)

        # Colour badge
        self.set_fill_color(r, g, b)
        self.set_text_color(255, 255, 255)
        self.set_font("Helvetica", "B", 10)
        badge_text = f"  {label.upper()}   Score: {score}/100   Severity: {severity}  "
        self.cell(0, 8, badge_text, fill=True, new_x="LMARGIN", new_y="NEXT")

        # Description
        self.set_text_color(52, 73, 94)
        self.set_font("Helvetica", "", 9)
        self.multi_cell(0, 5, description)
        self.ln(3)


def _build_pdf(data: PDFExportRequest) -> bytes:
    """Build the PDF document and return it as raw bytes."""
    pdf = SafeHavenPDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=20)

    # -- Location overview ---------------------------------------------------
    pdf.section_title("Location Overview")
    pdf.body_text(f"Address: {data.address or 'N/A'}")
    pdf.body_text(f"State: {data.state or 'N/A'}")
    pdf.body_text(f"Overall Risk Level: {data.overall_risk or 'Unknown'}")

    # -- Risk scores ---------------------------------------------------------
    pdf.section_title("Risk Assessment")
    for hazard in ("hurricane", "flood", "earthquake", "wildfire"):
        info = (data.risks or {}).get(hazard)
        if info:
            pdf.risk_badge(hazard, info.score, info.severity, info.description)

    # -- Recent earthquakes (if any) ----------------------------------------
    eqs = data.recent_earthquakes or []
    if eqs:
        pdf.section_title("Recent Earthquakes Nearby")
        for eq in eqs[:5]:
            mag = eq.magnitude or 0
            place = eq.place or "Unknown location"
            pdf.body_text(f"M{mag:.1f} -- {place}")

    # -- AI Report -----------------------------------------------------------
    report_text = data.report or ""
    if report_text:
        pdf.section_title("AI Safety Report")
        # Strip markdown headings for cleaner PDF rendering
        cleaned = report_text.replace("## ", "").replace("# ", "").replace("**", "")
        # fpdf2 handles encoding; split long text into paragraphs
        for paragraph in cleaned.split("\n\n"):
            paragraph = paragraph.strip()
            if paragraph:
                pdf.body_text(paragraph)

    # -- Disclaimer ----------------------------------------------------------
    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(149, 165, 166)
    pdf.multi_cell(
        0,
        4,
        "Disclaimer: This report is generated for informational purposes only and does "
        "not constitute professional emergency management advice. Always follow guidance "
        "from local authorities during an emergency.",
    )

    return pdf.output()


# ---------------------------------------------------------------------------
# Route
# ---------------------------------------------------------------------------

@router.post("/export-pdf")
async def export_pdf(payload: PDFExportRequest):
    """
    Generate a downloadable PDF report from risk-profile data and an AI report.
    """
    try:
        pdf_bytes = _build_pdf(payload)

        return StreamingResponse(
            io.BytesIO(pdf_bytes),
            media_type="application/pdf",
            headers={
                "Content-Disposition": 'attachment; filename="safehaven-report.pdf"'
            },
        )

    except Exception as exc:
        logger.error("PDF generation failed: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to generate PDF report.") from exc
