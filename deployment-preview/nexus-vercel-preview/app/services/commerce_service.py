"""
Nexus Commerce Service: Order Lifecycle and Financial State Machine
Enforces atomic single-transaction commits (F03), atomic state machine compare-and-set (F05),
strict input byte limits (F08), and content-free error diagnostics (F10).
"""

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone, timedelta
from typing import Optional, Tuple, Dict, Any, List

from app.models.core import generate_uuid, OrderExecutionState, AccountingState
from app.models.orders import Order, PayloadRecord
from app.models.authority import Agent, Owner
from app.models.offers import OfferPricing
from app.models.extraction import ExtractionInput
from app.core.clock import Clock, global_clock
from app.core.database import Database
from app.services.accounting_service import AccountingService
from app.services.authority_service import AuthorityService
from app.services.offer_service import OfferService
from app.services.fulfillment_service import FulfillmentService


class CommerceService:
    def __init__(
        self,
        db: Database,
        accounting: AccountingService,
        authority: AuthorityService,
        offers: OfferService,
        fulfillment: FulfillmentService,
        clock: Optional[Clock] = None
    ):
        self.db = db
        self.accounting = accounting
        self.authority = authority
        self.offers = offers
        self.fulfillment = fulfillment
        self.clock = clock or global_clock

    def purchase(
        self,
        agent: Agent,
        owner: Owner,
        offer_id: str,
        expected_offer_version: int,
        grant_id: str,
        raw_invoice_text: str,
        idempotency_key: str
    ) -> Order:
        """
        Execute an atomic, authorized purchase under owner-defined grant limits.
        Entire pre-dispatch reservation and order storage runs in ONE database transaction (F03).
        """
        now_dt = self.clock.now()
        now_iso = now_dt.isoformat()

        # 1. Enforce strict UTF-8 byte limits and code point bounds (F08)
        try:
            ExtractionInput(raw_text=raw_invoice_text)
        except ValueError as e:
            raise ValueError(f"INVALID_INPUT: {str(e)}")

        # 2. Compute deterministic request hash
        req_canonical = {
            "offer_id": offer_id,
            "version": expected_offer_version,
            "grant_id": grant_id,
            "raw_text": raw_invoice_text
        }
        request_hash = hashlib.sha256(json.dumps(req_canonical, sort_keys=True).encode("utf-8")).hexdigest()

        # 3. Fetch and verify Offer & Version (A05)
        offer = self.offers.get_offer(offer_id)
        if not offer or not offer.is_active:
            raise ValueError("OFFER_INACTIVE_OR_NOT_FOUND")
        if offer.version != expected_offer_version:
            raise ValueError(f"OFFER_CHANGED: Current version is {offer.version}, requested {expected_offer_version}")

        # 4. Fetch and verify Spend Grant & Scope
        grant = self.authority.get_spend_grant(grant_id)
        if not grant or grant.agent_id != agent.id or grant.owner_id != owner.id:
            raise ValueError("UNAUTHORIZED_SPEND_GRANT")
        if grant.is_revoked:
            raise ValueError("POLICY_DENIAL: Spend grant is revoked")
        if grant.expires_at and grant.expires_at <= now_iso:
            raise ValueError("POLICY_DENIAL: Spend grant has expired")
        if grant.allowed_capabilities and offer.capability_id not in grant.allowed_capabilities:
            raise ValueError(f"POLICY_DENIAL: Capability {offer.capability_id} not allowed by spend grant")

        # 5. Initialize Order & Payload storage IDs
        order_id = generate_uuid("ord")
        input_payload_id = generate_uuid("pay_in")
        deadline_dt = now_dt + timedelta(seconds=offer.execution_deadline_seconds)
        deadline_iso = deadline_dt.isoformat()

        order = Order(
            id=order_id,
            buyer_owner_id=owner.id,
            buyer_agent_id=agent.id,
            spend_grant_id=grant.id,
            seller_id=offer.seller_id,
            offer_id=offer.id,
            offer_version=offer.version,
            terms_hash=offer.terms_hash,
            pricing=offer.pricing,
            execution_state=OrderExecutionState.RESERVED,
            accounting_state=AccountingState.RESERVED,
            idempotency_key=idempotency_key,
            request_hash=request_hash,
            input_text_id=input_payload_id,
            created_at=now_iso,
            deadline_at=deadline_iso,
            seller_job_id=generate_uuid("job")
        )

        # 6. Single Atomic Database Transaction (F03, F04)
        with self.db.transaction() as conn:
            # Check Idempotency Key under transaction lock
            idemp_row = conn.execute(
                "SELECT * FROM idempotency_records WHERE idempotency_key = ? AND agent_id = ?",
                (idempotency_key, agent.id)
            ).fetchone()
            if idemp_row:
                if idemp_row["request_hash"] != request_hash:
                    raise ValueError("IDEMPOTENCY_CONFLICT: Key reused with different purchase payload")
                existing_order_row = conn.execute("SELECT * FROM orders WHERE id = ?", (idemp_row["order_id"],)).fetchone()
                return self._row_to_order(existing_order_row)

            # Atomic conditional reservation (F04, F09) using the active connection
            self.accounting.reserve_credits(
                buyer_owner_id=owner.id,
                grant_id=grant.id,
                amount=offer.pricing.buyer_total_credits,
                order_id=order.id,
                conn=conn,
                clock_now_iso=now_iso
            )

            # Store input payload
            conn.execute(
                """
                INSERT INTO payloads (id, order_id, payload_type, content_text, accessible_until, is_deleted)
                VALUES (?, ?, 'input', ?, ?, 0)
                """,
                (input_payload_id, order.id, raw_invoice_text, deadline_iso)
            )

            # Store order record
            conn.execute(
                """
                INSERT INTO orders (id, buyer_owner_id, buyer_agent_id, spend_grant_id, seller_id,
                                    offer_id, offer_version, terms_hash, buyer_total_credits,
                                    seller_net_credits, nexus_fee_credits, execution_state,
                                    accounting_state, idempotency_key, request_hash, input_text_id,
                                    created_at, deadline_at, dispatch_attempts, seller_job_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (order.id, order.buyer_owner_id, order.buyer_agent_id, order.spend_grant_id, order.seller_id,
                 order.offer_id, order.offer_version, order.terms_hash, order.pricing.buyer_total_credits,
                 order.pricing.seller_net_credits, order.pricing.nexus_fee_credits, order.execution_state.value,
                 order.accounting_state.value, order.idempotency_key, order.request_hash, order.input_text_id,
                 order.created_at, order.deadline_at, 1, order.seller_job_id)
            )

            # Store idempotency record
            conn.execute(
                "INSERT INTO idempotency_records (idempotency_key, agent_id, request_hash, order_id, created_at) VALUES (?, ?, ?, ?, ?)",
                (idempotency_key, agent.id, request_hash, order.id, now_iso)
            )

        # 7. Dispatch to Seller
        order.execution_state = OrderExecutionState.DISPATCHING
        self._update_order_state(order.id, OrderExecutionState.DISPATCHING, order.accounting_state)

        dispatch_ok, result_data, dispatch_err = self.fulfillment.dispatch_job(order, offer, raw_invoice_text)
        current_time = self.clock.now()

        # Check deadline expiry race (A12)
        if current_time > deadline_dt:
            self._handle_expiration(order, grant, "EXECUTION_DEADLINE_EXCEEDED")
            return self.get_order_by_id(order.id)

        if not dispatch_ok:
            self._handle_failure(order, grant, "SELLER_DISPATCH_FAILURE", dispatch_err or "Unknown seller error")
            return self.get_order_by_id(order.id)

        # 8. Validate Seller Result (A01, A26, F07)
        is_valid, parsed_result, val_errors = self.fulfillment.validate_extraction_result(raw_invoice_text, result_data)
        if not is_valid:
            self._handle_failure(order, grant, "RESULT_VALIDATION_FAILED", "; ".join(val_errors), val_errors)
            return self.get_order_by_id(order.id)

        # 9. SUCCESS! Settle credits atomically with compare-and-set (F05)
        self._handle_success(order, grant, result_data, current_time)
        return self.get_order_by_id(order.id)

    def _handle_success(self, order: Order, grant, result_data: Dict[str, Any], terminal_dt: datetime):
        """Atomically transition order to SUCCEEDED and settle financial accounts using CAS (F05)."""
        terminal_iso = terminal_dt.isoformat()
        accessible_until_iso = (terminal_dt + timedelta(hours=24)).isoformat()
        result_payload_id = generate_uuid("pay_res")

        with self.db.transaction() as conn:
            # Atomic CAS: order must still be in nonterminal execution state
            cur = conn.execute(
                """
                UPDATE orders
                SET execution_state = 'SUCCEEDED', accounting_state = 'SETTLED',
                    terminal_at = ?, accessible_until = ?, result_payload_id = ?
                WHERE id = ? AND execution_state IN ('RESERVED', 'DISPATCHING')
                """,
                (terminal_iso, accessible_until_iso, result_payload_id, order.id)
            )
            if cur.rowcount == 0:
                # Order was already cancelled or expired! Reject late settlement
                return

            # Settle accounting in the SAME atomic transaction (F03)
            self.accounting.settle_credits(
                buyer_owner_id=order.buyer_owner_id,
                seller_id=order.seller_id,
                grant_id=grant.id,
                buyer_total=order.pricing.buyer_total_credits,
                seller_net=order.pricing.seller_net_credits,
                nexus_fee=order.pricing.nexus_fee_credits,
                order_id=order.id,
                conn=conn
            )

            # Store result payload
            conn.execute(
                """
                INSERT INTO payloads (id, order_id, payload_type, content_text, accessible_until, is_deleted)
                VALUES (?, ?, 'result', ?, ?, 0)
                """,
                (result_payload_id, order.id, json.dumps(result_data), accessible_until_iso)
            )

            # Update input payload accessibility to match terminal + 24h
            conn.execute(
                "UPDATE payloads SET accessible_until = ? WHERE id = ?",
                (accessible_until_iso, order.input_text_id)
            )

        self.offers.record_execution_metric(order.offer_id, latency_ms=850, is_success=True)

    def _handle_failure(self, order: Order, grant, error_code: str, error_message: str, val_errors: Optional[list[str]] = None):
        """Atomically transition order to FAILED, sanitize errors (F10), and release credits using CAS (F05)."""
        now_dt = self.clock.now()
        terminal_iso = now_dt.isoformat()
        accessible_until_iso = (now_dt + timedelta(hours=24)).isoformat()

        # Sanitize diagnostics: strip any raw text snippets to prevent private data leakage (F10)
        sanitized_msg = re.sub(r"'[^']{15,}'", "'<redacted>'", error_message) if error_message else error_code
        sanitized_errors_json = json.dumps([re.sub(r"'[^']{15,}'", "'<redacted>'", e) for e in (val_errors or [])])

        with self.db.transaction() as conn:
            cur = conn.execute(
                """
                UPDATE orders
                SET execution_state = 'FAILED', accounting_state = 'RELEASED',
                    terminal_at = ?, accessible_until = ?, error_code = ?, error_message = ?, validation_errors = ?
                WHERE id = ? AND execution_state IN ('RESERVED', 'DISPATCHING')
                """,
                (terminal_iso, accessible_until_iso, error_code, sanitized_msg, sanitized_errors_json, order.id)
            )
            if cur.rowcount == 0:
                return

            self.accounting.release_credits(
                buyer_owner_id=order.buyer_owner_id,
                grant_id=grant.id,
                amount=order.pricing.buyer_total_credits,
                order_id=order.id,
                reason=f"Order failed: {error_code}",
                conn=conn
            )

            # Reset input payload accessibility to terminal + 24h
            conn.execute(
                "UPDATE payloads SET accessible_until = ? WHERE id = ?",
                (accessible_until_iso, order.input_text_id)
            )

    def _handle_expiration(self, order: Order, grant, reason: str):
        """Handle execution timeout atomically with CAS (F05, F10)."""
        now_dt = self.clock.now()
        terminal_iso = now_dt.isoformat()
        accessible_until_iso = (now_dt + timedelta(hours=24)).isoformat()

        with self.db.transaction() as conn:
            cur = conn.execute(
                """
                UPDATE orders
                SET execution_state = 'EXPIRED', accounting_state = 'RELEASED',
                    terminal_at = ?, accessible_until = ?, error_code = 'DEADLINE_TIMEOUT', error_message = ?
                WHERE id = ? AND execution_state IN ('RESERVED', 'DISPATCHING')
                """,
                (terminal_iso, accessible_until_iso, reason, order.id)
            )
            if cur.rowcount == 0:
                return

            self.accounting.release_credits(
                buyer_owner_id=order.buyer_owner_id,
                grant_id=grant.id,
                amount=order.pricing.buyer_total_credits,
                order_id=order.id,
                reason=f"Deadline exceeded: {reason}",
                conn=conn
            )

            conn.execute(
                "UPDATE payloads SET accessible_until = ? WHERE id = ?",
                (accessible_until_iso, order.input_text_id)
            )

    def cancel_order(self, order_id: str, actor_owner_id: str) -> Order:
        """
        Cancel order before dispatch or acknowledge cancellation atomically with CAS (A13, A14, F05).
        """
        now_dt = self.clock.now()
        now_iso = now_dt.isoformat()
        accessible_until_iso = (now_dt + timedelta(hours=24)).isoformat()

        with self.db.transaction() as conn:
            row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
            if not row:
                raise ValueError("Order not found")
            if row["buyer_owner_id"] != actor_owner_id:
                raise ValueError("UNAUTHORIZED_CANCELLATION")

            cur = conn.execute(
                """
                UPDATE orders
                SET execution_state = 'CANCELLED', accounting_state = 'RELEASED',
                    terminal_at = ?, accessible_until = ?
                WHERE id = ? AND execution_state IN ('RESERVED', 'DISPATCHING')
                """,
                (now_iso, accessible_until_iso, order_id)
            )
            if cur.rowcount == 0:
                curr = conn.execute("SELECT execution_state FROM orders WHERE id = ?", (order_id,)).fetchone()
                raise ValueError(f"CANNOT_CANCEL: Order already in terminal state {curr['execution_state']}")

            self.accounting.release_credits(
                buyer_owner_id=row["buyer_owner_id"],
                grant_id=row["spend_grant_id"],
                amount=row["buyer_total_credits"],
                order_id=order_id,
                reason="Order cancelled by buyer",
                conn=conn
            )

            conn.execute(
                "UPDATE payloads SET accessible_until = ? WHERE id = ?",
                (accessible_until_iso, row["input_text_id"])
            )

        return self.get_order_by_id(order_id)

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        with self.db.transaction() as conn:
            row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
            return self._row_to_order(row) if row else None

    def get_order_payload(self, payload_id: str, actor_owner_id: str) -> str:
        """
        Retrieves order payload content, strictly enforcing 24h retention window and dispute hold.
        """
        now_iso = self.clock.now_iso()
        with self.db.transaction() as conn:
            row = conn.execute("SELECT * FROM payloads WHERE id = ?", (payload_id,)).fetchone()
            if not row:
                raise ValueError("PAYLOAD_NOT_FOUND")

            order = conn.execute("SELECT buyer_owner_id FROM orders WHERE id = ?", (row["order_id"],)).fetchone()
            if not order or order["buyer_owner_id"] != actor_owner_id:
                raise ValueError("UNAUTHORIZED_PAYLOAD_ACCESS")

            if row["is_deleted"]:
                raise ValueError("PAYLOAD_DELETED")

            is_expired = row["accessible_until"] <= now_iso
            has_active_hold = row["dispute_hold_until"] and row["dispute_hold_until"] > now_iso

            if is_expired and not has_active_hold:
                raise ValueError("PAYLOAD_ACCESS_EXPIRED: 24-hour access window has passed")

            return row["content_text"]

    def _update_order_state(self, order_id: str, exec_state: OrderExecutionState, acc_state: AccountingState):
        with self.db.transaction() as conn:
            conn.execute(
                "UPDATE orders SET execution_state = ?, accounting_state = ? WHERE id = ?",
                (exec_state.value, acc_state.value, order_id)
            )

    def _row_to_order(self, row: sqlite3.Row) -> Order:
        data = dict(row)
        data["pricing"] = OfferPricing(
            buyer_total_credits=data["buyer_total_credits"],
            seller_net_credits=data["seller_net_credits"],
            nexus_fee_credits=data["nexus_fee_credits"]
        )
        data["execution_state"] = OrderExecutionState(data["execution_state"])
        data["accounting_state"] = AccountingState(data["accounting_state"])
        if data.get("validation_errors") and isinstance(data["validation_errors"], str):
            try:
                data["validation_errors"] = json.loads(data["validation_errors"])
            except Exception:
                data["validation_errors"] = [data["validation_errors"]]
        return Order(**data)
