"""
SafeHaven configuration module.

Loads environment variables from a .env file and exposes them as module-level
constants.  Every variable falls back to an empty string so the application can
start even when keys are missing (features that require them will return
graceful errors instead).
"""

import os
from dotenv import load_dotenv

load_dotenv(override=True)

GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
STRIPE_SECRET_KEY: str = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_PRICE_ID: str = os.getenv("STRIPE_PRICE_ID", "")
