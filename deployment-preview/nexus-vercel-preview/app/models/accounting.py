"""
Nexus Double-Entry Test Credit Accounting Models
Guarantees balanced credit preservation across all financial operations.
"""

from typing import List, Literal, Optional
from pydantic import BaseModel, Field
from app.models.core import utc_now_iso


class AccountBalance(BaseModel):
    account_id: str = Field(..., description="Entity account ID (owner ID, seller ID, or 'platform_fees')")
    account_type: Literal["BUYER", "SELLER", "PLATFORM_FEES"]
    available_credits: int = Field(default=0, ge=0)
    reserved_credits: int = Field(default=0, ge=0)


class LedgerPosting(BaseModel):
    account_id: str
    account_type: str
    amount: int = Field(..., description="Positive for credit, negative for debit")
    balance_type: Literal["AVAILABLE", "RESERVED"]


class JournalEntry(BaseModel):
    id: str
    order_id: Optional[str] = None
    operation_type: Literal["INITIAL_GRANT", "RESERVATION", "SETTLEMENT", "RELEASE", "REVERSAL"]
    postings: List[LedgerPosting]
    created_at: str = Field(default_factory=utc_now_iso)
    reason: Optional[str] = None

    def verify_balanced(self):
        """Total debits and credits across all accounts must sum to zero."""
        total = sum(p.amount for p in self.postings)
        if total != 0:
            raise ValueError(f"Unbalanced journal entry '{self.id}': sum of postings is {total}, must be 0")

