"""
Nexus Core Types and Enums
"""

import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Annotated
from pydantic import Field, PlainSerializer


def generate_uuid(prefix: str = "") -> str:
    """Generate a prefixed random UUID."""
    raw = uuid.uuid4().hex[:16]
    return f"{prefix}_{raw}" if prefix else raw


def utc_now_iso() -> str:
    """Current UTC timestamp in ISO 8601 format."""
    return datetime.now(timezone.utc).isoformat()


class OrderExecutionState(str, Enum):
    """Execution state machine states."""
    RESERVED = "RESERVED"          # Order created, credits locked, awaiting dispatch
    DISPATCHING = "DISPATCHING"    # Sent to durable dispatcher, claiming execution
    RUNNING = "RUNNING"            # Seller acknowledged job and is processing
    SUCCEEDED = "SUCCEEDED"        # Result accepted and validated within deadline
    FAILED = "FAILED"              # Seller returned error or invalid schema
    EXPIRED = "EXPIRED"            # Execution deadline elapsed before accepted result
    CANCELLED = "CANCELLED"        # Cancelled before dispatch or acknowledged by seller


class AccountingState(str, Enum):
    """Financial ledger state machine states."""
    RESERVED = "RESERVED"          # Test credits reserved from buyer wallet and grant
    SETTLED = "SETTLED"            # Credits permanently transferred to seller net and fee
    RELEASED = "RELEASED"          # Credits returned to buyer wallet/grant (fail/expire/cancel)
    REVERSED = "REVERSED"          # Human operator approved a post-settlement dispute refund


class DisputeStatus(str, Enum):
    """Dispute lifecycle states."""
    OPEN = "OPEN"
    RESOLVED_REFUNDED = "RESOLVED_REFUNDED"
    RESOLVED_REJECTED = "RESOLVED_REJECTED"

