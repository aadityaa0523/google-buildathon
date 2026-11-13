"""
Nexus Authority and Identity Models
Manages human owners, registered autonomous agents, hashed credentials, and spend grants.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from app.models.core import utc_now_iso


class Owner(BaseModel):
    id: str = Field(..., description="Unique owner identifier (e.g. 'usr_aadityaa')")
    email: str
    name: str
    created_at: str = Field(default_factory=utc_now_iso)


class Agent(BaseModel):
    id: str = Field(..., description="Unique agent identifier (e.g. 'agt_purchaser_01')")
    owner_id: str
    name: str
    is_active: bool = True
    created_at: str = Field(default_factory=utc_now_iso)


class AgentCredential(BaseModel):
    id: str
    agent_id: str
    owner_id: str
    key_prefix: str
    hashed_secret: str
    created_at: str = Field(default_factory=utc_now_iso)
    revoked_at: Optional[str] = None


class OwnerCredential(BaseModel):
    id: str
    owner_id: str
    key_prefix: str
    hashed_secret: str
    created_at: str = Field(default_factory=utc_now_iso)
    revoked_at: Optional[str] = None


class SpendGrant(BaseModel):
    """
    Owner-authorized spend allowance governing an autonomous agent.
    All credits are integer test-credit units.
    """
    id: str = Field(..., description="Unique spend grant ID (e.g. 'grt_5000_invoices')")
    owner_id: str
    agent_id: str
    max_allowance_credits: int = Field(..., ge=1, description="Total lifetime credit budget granted to this agent")
    spent_credits: int = Field(default=0, ge=0, description="Credits permanently consumed by settled orders")
    reserved_credits: int = Field(default=0, ge=0, description="Credits currently locked in in-flight orders")
    per_order_max_credits: int = Field(..., ge=1, description="Maximum single-transaction purchase ceiling")
    allowed_capabilities: List[str] = Field(default=["invoice.extract.v1"], description="List of capability IDs agent may purchase")
    expires_at: Optional[str] = None
    is_revoked: bool = False

    @property
    def available_credits(self) -> int:
        """Available headroom remaining under this grant."""
        return max(0, self.max_allowance_credits - (self.spent_credits + self.reserved_credits))

    def can_reserve(self, amount: int, capability_id: str) -> tuple[bool, Optional[str]]:
        """Validate if grant allows a new purchase of given amount."""
        if self.is_revoked:
            return False, "GRANT_REVOKED"
        if capability_id not in self.allowed_capabilities:
            return False, "CAPABILITY_NOT_PERMITTED_UNDER_GRANT"
        if amount > self.per_order_max_credits:
            return False, f"AMOUNT_EXCEEDS_PER_ORDER_CAP ({amount} > {self.per_order_max_credits})"
        if amount > self.available_credits:
            return False, f"INSUFFICIENT_GRANT_HEADROOM (Required {amount}, available {self.available_credits})"
        return True, None

