"""
Nexus Accountability Models: Order-Backed Reviews and Disputes
"""

from typing import Optional
from pydantic import BaseModel, Field
from app.models.core import DisputeStatus, utc_now_iso


class Review(BaseModel):
    id: str
    order_id: str = Field(..., description="Order ID that this review is tied to (must be executed)")
    buyer_owner_id: str
    seller_id: str
    rating: int = Field(..., ge=1, le=5, description="1 to 5 stars")
    comment: str = Field(..., max_length=1000)
    is_common_owner: bool = Field(default=False, description="True if buyer and seller share owner (excluded from public score)")
    created_at: str = Field(default_factory=utc_now_iso)
    updated_at: str = Field(default_factory=utc_now_iso)


class Dispute(BaseModel):
    id: str
    order_id: str
    buyer_owner_id: str
    seller_id: str
    reason: str = Field(..., description="Declared reason for dispute, e.g. WRONG_TOTAL, HALLUCINATED_FIELD")
    details: str = Field(..., max_length=2000)
    status: DisputeStatus = DisputeStatus.OPEN
    evidence_hold_until: str = Field(..., description="Preserves necessary evidence for dispute review (up to 7 days)")
    created_at: str = Field(default_factory=utc_now_iso)
    resolved_at: Optional[str] = None
    operator_reason: Optional[str] = None

