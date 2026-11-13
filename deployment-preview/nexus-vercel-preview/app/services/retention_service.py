"""
Nexus Retention and Payload Expiry Service
Enforces strict 24-hour access expiration and executes active data deletion sweeps.
"""

from typing import Optional
from app.core.clock import Clock, global_clock
from app.core.database import Database


class RetentionService:
    def __init__(self, db: Database, clock: Optional[Clock] = None):
        self.db = db
        self.clock = clock or global_clock

    def sweep_expired_payloads(self) -> int:
        """
        Active deletion sweeper: scrubs raw content from payloads past their 24h retention window,
        unless preserved under an active dispute hold (A21, A22).
        Returns count of purged payload records.
        """
        now_iso = self.clock.now_iso()
        with self.db.transaction() as conn:
            rows = conn.execute(
                """
                SELECT id FROM payloads
                WHERE is_deleted = 0
                  AND accessible_until <= ?
                  AND (dispute_hold_until IS NULL OR dispute_hold_until <= ?)
                """,
                (now_iso, now_iso)
            ).fetchall()

            count = len(rows)
            for r in rows:
                conn.execute(
                    """
                    UPDATE payloads
                    SET content_text = '[PURGED_POST_24H_RETENTION_EXPIRY]', is_deleted = 1
                    WHERE id = ?
                    """,
                    (r["id"],)
                )
            return count

