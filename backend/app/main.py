"""
SafeHaven API -- FastAPI application entry point.

Run with:
    uvicorn app.main:app --reload
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    geocode,
    risk_profile,
    shelters,
    ai_report,
    emergency_contacts,
    donations,
    export_pdf,
    noaa_alerts,
    historical_disasters,
)

logger = logging.getLogger("safehaven")
logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Application startup / shutdown lifecycle."""
    logger.info("SafeHaven API running")
    yield
    logger.info("SafeHaven API shutting down")


app = FastAPI(
    title="SafeHaven API",
    description="AI-powered disaster resilience tool",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# CORS -- restrict to our frontend domains
# ---------------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://safehaven.tools",
        "https://www.safehaven.tools",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Mount routers -- every route is served under the /api prefix
# ---------------------------------------------------------------------------
app.include_router(geocode.router, prefix="/api", tags=["Geocoding"])
app.include_router(risk_profile.router, prefix="/api", tags=["Risk Profile"])
app.include_router(shelters.router, prefix="/api", tags=["Shelters"])
app.include_router(ai_report.router, prefix="/api", tags=["AI Report"])
app.include_router(emergency_contacts.router, prefix="/api", tags=["Emergency Contacts"])
app.include_router(donations.router, prefix="/api", tags=["Donations"])
app.include_router(export_pdf.router, prefix="/api", tags=["PDF Export"])
app.include_router(noaa_alerts.router, prefix="/api", tags=["NOAA Alerts"])
app.include_router(historical_disasters.router, prefix="/api", tags=["Historical Disasters"])


@app.get("/", tags=["Health"])
async def health_check():
    """Simple health-check endpoint."""
    return {"status": "ok", "service": "SafeHaven API"}
