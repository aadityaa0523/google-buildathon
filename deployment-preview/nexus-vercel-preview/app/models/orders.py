"""
Nexus Orders and Lifecycle Models
Tracks state transitions, locked terms, and payload retention boundaries.
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from app.models.core import OrderExecutionState, AccountingState, utc_now_iso
from app.models.offers import OfferPricing


class Order(BaseModel):
    id: str = Field(..., description="Unique order identifier (e.g. 'ord_88410')")
    buyer_owner_id: str
    buyer_agent_id: str
    spend_grant_id: str
    
    seller_id: str
    offer_id: str
    offer_version: int
    terms_hash: str = Field(..., description="Locked SHA-256 hash of agreed terms")
    pricing: OfferPricing
    
    execution_state: OrderExecutionState = OrderExecutionState.RESERVED
    accounting_state: AccountingState = AccountingState.RESERVED
    
    idempotency_key: str
    request_hash: str
    
    # Payload references (separated from metadata for data isolation and retention)
    input_text_id: str
    result_payload_id: Optional[str] = None
    
    created_at: str = Field(default_factory=utc_now_iso)
    deadline_at: str = Field(..., description="Absolute ISO timestamp by which result must be accepted")
    terminal_at: Optional[str] = None
    accessible_until: Optional[str] = None
    
    # Dispatch tracking
    dispatch_attempts: int = 0
    seller_job_id: Optional[str] = None
    
    # Outcome diagnostics
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    validation_errors: Optional[list[str]] = None


class PayloadRecord(BaseModel):
    """
    Restricted payload record storing raw invoice input or output JSON.
    Access strictly expires at accessible_until (24h post execution-terminal).
    """
    id: str
    order_id: str
    payload_type: str  # "input" or "result"
    content_text: str  # UTF-8 text or serialized JSON string
    accessible_until: str
    is_deleted: bool = False
    dispute_hold_until: Optional[str] = None

