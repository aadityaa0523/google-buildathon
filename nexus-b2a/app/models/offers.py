"""
Nexus Offers and Seller Models
Defines registered SaaS sellers, versioned fixed-price offers, and execution policies.
"""

import hashlib
import json
from typing import Optional
from pydantic import BaseModel, Field, model_validator
from app.models.core import utc_now_iso


class OfferPricing(BaseModel):
    """
    Fixed integer test-credit price breakdown for an offer.
    Invariant: buyer_total_credits == seller_net_credits + nexus_fee_credits.
    """
    buyer_total_credits: int = Field(..., ge=1, description="Total amount charged to buyer wallet")
    seller_net_credits: int = Field(..., ge=0, description="Amount credited to seller upon success")
    nexus_fee_credits: int = Field(..., ge=0, description="Nexus marketplace commission fee")

    @model_validator(mode="after")
    def verify_pricing_balance(self):
        if self.buyer_total_credits != (self.seller_net_credits + self.nexus_fee_credits):
            raise ValueError(
                f"Pricing invariant violated: buyer_total ({self.buyer_total_credits}) must equal "
                f"seller_net ({self.seller_net_credits}) + nexus_fee ({self.nexus_fee_credits})"
            )
        return self


class SellerProfile(BaseModel):
    id: str = Field(..., description="Unique seller organization ID (e.g. 'sel_docuextract_corp')")
    name: str
    owner_id: str = Field(..., description="Owner account ID responsible for this seller")
    verified_endpoint: bool = False
    created_at: str = Field(default_factory=utc_now_iso)


class Offer(BaseModel):
    """
    Versioned, immutable fixed-price capability offer published by a seller.
    """
    id: str = Field(..., description="Unique offer identifier (e.g. 'ofr_fast_extract')")
    seller_id: str
    capability_id: str = "invoice.extract.v1"
    version: int = Field(default=1, ge=1)
    title: str
    description: str
    pricing: OfferPricing
    execution_deadline_seconds: int = Field(default=30, ge=5, le=300)
    endpoint_url: str = Field(..., description="Seller webhook URL invoked by Nexus")
    endpoint_secret: str = Field(..., description="Secret used to sign payloads to seller and verify callbacks")
    is_active: bool = True
    created_at: str = Field(default_factory=utc_now_iso)

    # Performance and quality metrics (derived from real order history)
    total_completed_orders: int = 0
    p95_latency_ms: int = 1200
    success_rate_pct: float = 100.0
    average_rating: float = 0.0
    rating_count: int = 0

    @property
    def terms_hash(self) -> str:
        """Cryptographic hash of the immutable commercial terms."""
        canonical_terms = {
            "offer_id": self.id,
            "version": self.version,
            "capability_id": self.capability_id,
            "buyer_total_credits": self.pricing.buyer_total_credits,
            "seller_net_credits": self.pricing.seller_net_credits,
            "nexus_fee_credits": self.pricing.nexus_fee_credits,
            "execution_deadline_seconds": self.execution_deadline_seconds,
            "endpoint_url": self.endpoint_url
        }
        encoded = json.dumps(canonical_terms, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def to_public(self) -> "PublicOffer":
        return PublicOffer(
            id=self.id,
            seller_id=self.seller_id,
            capability_id=self.capability_id,
            version=self.version,
            title=self.title,
            description=self.description,
            pricing=self.pricing,
            execution_deadline_seconds=self.execution_deadline_seconds,
            is_active=self.is_active,
            created_at=self.created_at,
            total_completed_orders=self.total_completed_orders,
            p95_latency_ms=self.p95_latency_ms,
            success_rate_pct=self.success_rate_pct,
            average_rating=self.average_rating,
            rating_count=self.rating_count
        )


class PublicOffer(BaseModel):
    """
    Publicly visible offer view safe for external discovery (REST, MCP, and UI).
    Strictly omits endpoint_secret and private internal seller dispatch credentials (F02).
    """
    id: str
    seller_id: str
    capability_id: str
    version: int
    title: str
    description: str
    pricing: OfferPricing
    execution_deadline_seconds: int
    is_active: bool
    created_at: str
    total_completed_orders: int
    p95_latency_ms: int
    success_rate_pct: float
    average_rating: float
    rating_count: int


