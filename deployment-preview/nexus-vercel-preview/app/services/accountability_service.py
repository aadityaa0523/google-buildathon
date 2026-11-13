"""
Nexus Accountability Service: Reviews, Disputes, and Operator Adjudication
"""

from datetime import datetime, timezone, timedelta
from typing import Optional, List
from app.models.core import generate_uuid, DisputeStatus, OrderExecutionState, utc_now_iso
from app.models.accountability import Review, Dispute
from app.core.clock import Clock, global_clock
from app.core.database import Database
from app.services.accounting_service import AccountingService


class AccountabilityService:
    def __init__(self, db: Database, accounting: AccountingService, clock: Optional[Clock] = None):
        self.db = db
        self.accounting = accounting
        self.clock = clock or global_clock

    def submit_review(self, order_id: str, buyer_owner_id: str, rating: int, comment: str) -> Review:
        """
        Submit an order-backed review. Self-dealing trades (common owner) are excluded from aggregate score.
        """
        now_iso = self.clock.now_iso()
        with self.db.transaction() as conn:
            # 1. Fetch order and verify eligibility (A18)
            order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
            if not order:
                raise ValueError("Order not found")
            if order["buyer_owner_id"] != buyer_owner_id:
                raise ValueError("UNAUTHORIZED_REVIEW: Only buyer owner can review")
            if order["execution_state"] not in (OrderExecutionState.SUCCEEDED.value, OrderExecutionState.FAILED.value):
                raise ValueError("CANNOT_REVIEW: Order has not reached terminal execution")

            # Check if review already exists
            existing = conn.execute("SELECT id FROM reviews WHERE order_id = ?", (order_id,)).fetchone()
            if existing:
                raise ValueError("DUPLICATE_REVIEW: Order already reviewed")

            # 2. Check common ownership
            seller = conn.execute("SELECT owner_id FROM sellers WHERE id = ?", (order["seller_id"],)).fetchone()
            is_common_owner = (seller["owner_id"] == buyer_owner_id)

            review_id = generate_uuid("rev")
            review = Review(
                id=review_id,
                order_id=order_id,
                buyer_owner_id=buyer_owner_id,
                seller_id=order["seller_id"],
                rating=rating,
                comment=comment,
                is_common_owner=is_common_owner,
                created_at=now_iso,
                updated_at=now_iso
            )

            conn.execute(
                """
                INSERT INTO reviews (id, order_id, buyer_owner_id, seller_id, rating, comment, is_common_owner, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (review.id, review.order_id, review.buyer_owner_id, review.seller_id, review.rating,
                 review.comment, int(review.is_common_owner), review.created_at, review.updated_at)
            )

            # 3. Recalculate seller public score (excluding common owner reviews)
            stats = conn.execute(
                """
                SELECT COUNT(*) as count, AVG(rating) as avg_rating
                FROM reviews
                WHERE seller_id = ? AND is_common_owner = 0
                """,
                (order["seller_id"],)
            ).fetchone()
            
            avg_rating = round(stats["avg_rating"] or 0.0, 2)
            count = stats["count"]

            conn.execute(
                "UPDATE offers SET average_rating = ?, rating_count = ? WHERE seller_id = ?",
                (avg_rating, count, order["seller_id"])
            )

            return review

    def open_dispute(self, order_id: str, buyer_owner_id: str, reason: str, details: str) -> Dispute:
        """
        Open a commercial dispute within 24 hours of order completion.
        Places a 7-day evidence hold on relevant payloads.
        """
        now_dt = self.clock.now()
        now_iso = now_dt.isoformat()
        hold_dt = now_dt + timedelta(days=7)
        hold_iso = hold_dt.isoformat()

        with self.db.transaction() as conn:
            order = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
            if not order:
                raise ValueError("Order not found")
            if order["buyer_owner_id"] != buyer_owner_id:
                raise ValueError("UNAUTHORIZED_DISPUTE: Only buyer owner can open dispute")

            # Check 24h window
            terminal_at = order["terminal_at"]
            if not terminal_at:
                raise ValueError("Order has not finished execution")
            term_dt = datetime.fromisoformat(terminal_at)
            if (now_dt - term_dt) > timedelta(hours=24):
                raise ValueError("DISPUTE_WINDOW_EXPIRED: Disputes must be raised within 24 hours of execution")

            # Only settled orders can be disputed for refund (F06)
            if order["accounting_state"] != "SETTLED":
                raise ValueError(f"CANNOT_DISPUTE_UNSETTLED_ORDER: Order accounting state is '{order['accounting_state']}'. Unsettled orders have already released their reservation.")

            existing = conn.execute("SELECT id FROM disputes WHERE order_id = ?", (order_id,)).fetchone()
            if existing:
                raise ValueError("DUPLICATE_DISPUTE: Dispute already open for this order")

            dispute_id = generate_uuid("dsp")
            dispute = Dispute(
                id=dispute_id,
                order_id=order_id,
                buyer_owner_id=buyer_owner_id,
                seller_id=order["seller_id"],
                reason=reason,
                details=details,
                status=DisputeStatus.OPEN,
                evidence_hold_until=hold_iso,
                created_at=now_iso
            )

            conn.execute(
                """
                INSERT INTO disputes (id, order_id, buyer_owner_id, seller_id, reason, details, status, evidence_hold_until, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (dispute.id, dispute.order_id, dispute.buyer_owner_id, dispute.seller_id, dispute.reason,
                 dispute.details, dispute.status.value, dispute.evidence_hold_until, dispute.created_at)
            )

            # Apply evidence hold to payloads
            conn.execute(
                "UPDATE payloads SET dispute_hold_until = ? WHERE order_id = ?",
                (hold_iso, order_id)
            )

            return dispute

    def adjudicate_dispute(self, dispute_id: str, approved: bool, operator_reason: str) -> Dispute:
        """
        Human operator adjudication. If approved, executes financial reversal in one atomic transaction (A19, F06).
        """
        now_iso = self.clock.now_iso()
        with self.db.transaction() as conn:
            dispute_row = conn.execute("SELECT * FROM disputes WHERE id = ?", (dispute_id,)).fetchone()
            if not dispute_row:
                raise ValueError("Dispute not found")
            if dispute_row["status"] != DisputeStatus.OPEN.value:
                raise ValueError("DISPUTE_ALREADY_RESOLVED")

            order = conn.execute("SELECT * FROM orders WHERE id = ?", (dispute_row["order_id"],)).fetchone()
            if not order:
                raise ValueError("Order not found")

            # 1. Atomically claim dispute transition with CAS (F06)
            new_status = DisputeStatus.RESOLVED_REFUNDED if approved else DisputeStatus.RESOLVED_REJECTED
            cur_disp = conn.execute(
                """
                UPDATE disputes
                SET status = ?, resolved_at = ?, operator_reason = ?
                WHERE id = ? AND status = 'OPEN'
                """,
                (new_status.value, now_iso, operator_reason, dispute_id)
            )
            if cur_disp.rowcount == 0:
                raise ValueError("DISPUTE_ALREADY_RESOLVED")

            # 2. If approved, atomically claim order state transition to REVERSED (F06, F13)
            if approved:
                cur_ord = conn.execute(
                    """
                    UPDATE orders
                    SET accounting_state = 'REVERSED'
                    WHERE id = ? AND accounting_state = 'SETTLED' AND execution_state = 'SUCCEEDED'
                    """,
                    (order["id"],)
                )
                if cur_ord.rowcount == 0:
                    raise ValueError(f"ORDER_NOT_REFUNDABLE: Order accounting state is '{order['accounting_state']}' (must be 'SETTLED' and unreversed to refund)")

                # Execute financial reversal inside the SAME transaction (F03, F06)
                self.accounting.reverse_credits(
                    buyer_owner_id=order["buyer_owner_id"],
                    seller_id=order["seller_id"],
                    grant_id=order["spend_grant_id"],
                    buyer_total=order["buyer_total_credits"],
                    seller_net=order["seller_net_credits"],
                    nexus_fee=order["nexus_fee_credits"],
                    order_id=order["id"],
                    reason=f"Dispute {dispute_id} approved: {operator_reason}",
                    conn=conn
                )

            updated = conn.execute("SELECT * FROM disputes WHERE id = ?", (dispute_id,)).fetchone()
            data = dict(updated)
            data["status"] = DisputeStatus(data["status"])
            return Dispute(**data)

