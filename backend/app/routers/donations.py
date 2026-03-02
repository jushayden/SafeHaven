"""
/api/create-checkout-session -- Create a Stripe Checkout session for donations.
"""

from __future__ import annotations

import logging
from typing import Optional

import stripe
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.config import STRIPE_SECRET_KEY, STRIPE_PRICE_ID

logger = logging.getLogger("safehaven.donations")
router = APIRouter()


class DonationRequest(BaseModel):
    """Payload for creating a Stripe Checkout session."""
    amount: Optional[int] = Field(
        default=1000,
        description="Donation amount in cents (e.g. 1000 = $10.00)",
    )
    success_url: Optional[str] = "http://localhost:3000/donation-success"
    cancel_url: Optional[str] = "http://localhost:3000/donation-cancel"


@router.post("/create-checkout-session")
async def create_checkout_session(payload: DonationRequest):
    """
    Create a Stripe Checkout session for a one-time donation.

    If ``STRIPE_PRICE_ID`` is set, it is used as a pre-configured price object.
    Otherwise, a dynamic price is created from the *amount* in the request body
    (in cents, e.g. 1000 = $10).

    Returns ``{ "url": "<checkout page URL>", "session_id": "..." }``.
    """
    if not STRIPE_SECRET_KEY:
        raise HTTPException(
            status_code=503,
            detail="Stripe is not configured. Set STRIPE_SECRET_KEY in your environment.",
        )

    stripe.api_key = STRIPE_SECRET_KEY

    try:
        # Build line-item depending on whether a preset price exists
        if STRIPE_PRICE_ID:
            line_items = [{"price": STRIPE_PRICE_ID, "quantity": 1}]
        else:
            amount = payload.amount if payload.amount and payload.amount > 0 else 1000
            line_items = [
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {
                            "name": "SafeHaven Disaster Relief Donation",
                            "description": "Your donation helps communities prepare for and recover from natural disasters.",
                        },
                        "unit_amount": amount,
                    },
                    "quantity": 1,
                }
            ]

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=payload.success_url,
            cancel_url=payload.cancel_url,
        )

        return {
            "url": session.url,
            "session_id": session.id,
        }

    except stripe.error.StripeError as exc:
        logger.error("Stripe error: %s", exc)
        raise HTTPException(status_code=502, detail=f"Stripe error: {exc.user_message or str(exc)}") from exc
    except Exception as exc:
        logger.error("Unexpected error creating checkout session: %s", exc)
        raise HTTPException(status_code=500, detail="Failed to create checkout session.") from exc
