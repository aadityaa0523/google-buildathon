"""
Nexus Accounting Service
Manages balanced double-entry test credit ledger, wallets, and grant tracking.
Features atomic conditional updates to prevent race conditions and overspend (F03, F04, F09).
"""

import json
import sqlite3
from datetime import datetime, timezone
from contextlib import contextmanager
from typing import Optional
from app.models.core import generate_uuid, AccountingState, utc_now_iso
from app.models.accounting import JournalEntry, LedgerPosting
from app.core.database import Database


class AccountingService:
    def __init__(self, db: Database):
        self.db = db

    @contextmanager
    def _use_conn(self, conn: Optional[sqlite3.Connection] = None):
        if conn is not None:
            yield conn
        else:
            with self.db.transaction() as new_conn:
                yield new_conn

    def get_or_create_account(self, account_id: str, account_type: str, conn: Optional[sqlite3.Connection] = None) -> dict:
        with self._use_conn(conn) as c:
            row = c.execute("SELECT * FROM accounts WHERE account_id = ?", (account_id,)).fetchone()
            if row:
                return dict(row)
            c.execute(
                "INSERT INTO accounts (account_id, account_type, available_credits, reserved_credits) VALUES (?, ?, ?, ?)",
                (account_id, account_type, 0, 0)
            )
            return {"account_id": account_id, "account_type": account_type, "available_credits": 0, "reserved_credits": 0}

    def seed_wallet(self, owner_id: str, credits_amount: int, conn: Optional[sqlite3.Connection] = None) -> int:
        """Seed nonredeemable test credits to an owner wallet."""
        with self._use_conn(conn) as c:
            c.execute(
                """
                INSERT INTO accounts (account_id, account_type, available_credits, reserved_credits)
                VALUES (?, 'BUYER', ?, 0)
                ON CONFLICT(account_id) DO UPDATE SET available_credits = available_credits + ?
                """,
                (owner_id, credits_amount, credits_amount)
            )
            entry = JournalEntry(
                id=generate_uuid("jrn"),
                operation_type="INITIAL_GRANT",
                postings=[
                    LedgerPosting(account_id="nexus_treasury", account_type="TREASURY", amount=-credits_amount, balance_type="AVAILABLE"),
                    LedgerPosting(account_id=owner_id, account_type="BUYER", amount=credits_amount, balance_type="AVAILABLE")
                ],
                reason=f"Admin seed of {credits_amount} test credits"
            )
            entry.verify_balanced()
            c.execute(
                "INSERT INTO journal (id, operation_type, postings_json, created_at, reason) VALUES (?, ?, ?, ?, ?)",
                (entry.id, entry.operation_type, json.dumps([p.model_dump() for p in entry.postings]), entry.created_at, entry.reason)
            )
            row = c.execute("SELECT available_credits FROM accounts WHERE account_id = ?", (owner_id,)).fetchone()
            return row["available_credits"]

    def reserve_credits(
        self,
        buyer_owner_id: str,
        grant_id: str,
        amount: int,
        order_id: str,
        conn: Optional[sqlite3.Connection] = None,
        clock_now_iso: Optional[str] = None
    ) -> bool:
        """
        Atomically reserve credits from buyer wallet and spend grant in one transaction.
        Enforces atomic conditional checks: expiry, revocation, allowance, and wallet balance (F04, F09).
        """
        now_iso = clock_now_iso or utc_now_iso()
        cur_dt = datetime.fromisoformat(now_iso)
        if cur_dt.tzinfo is None:
            cur_dt = cur_dt.replace(tzinfo=timezone.utc)
        else:
            cur_dt = cur_dt.astimezone(timezone.utc)
        cur_utc_iso = cur_dt.isoformat()

        with self._use_conn(conn) as c:
            # 0. Pre-flight grant validation with UTC datetime normalization (F09)
            grant_row = c.execute("SELECT * FROM spend_grants WHERE id = ?", (grant_id,)).fetchone()
            if not grant_row:
                raise ValueError("SPEND_GRANT_NOT_FOUND")
            if grant_row["is_revoked"]:
                raise ValueError("POLICY_DENIAL: Spend grant is revoked")
            if grant_row["expires_at"]:
                exp_dt = datetime.fromisoformat(grant_row["expires_at"])
                if exp_dt.tzinfo is None:
                    exp_dt = exp_dt.replace(tzinfo=timezone.utc)
                else:
                    exp_dt = exp_dt.astimezone(timezone.utc)
                if exp_dt <= cur_dt:
                    raise ValueError("POLICY_DENIAL: Spend grant has expired")
            if amount > grant_row["per_order_max_credits"]:
                raise ValueError(f"POLICY_DENIAL: AMOUNT_EXCEEDS_PER_ORDER_CAP: Order amount ({amount}) exceeds per-order cap ({grant_row['per_order_max_credits']})")

            # 1. Atomic conditional update on spend grant headroom (F04)
            cur_grant = c.execute(
                """
                UPDATE spend_grants
                SET reserved_credits = reserved_credits + ?
                WHERE id = ?
                  AND is_revoked = 0
                  AND (spent_credits + reserved_credits + ?) <= max_allowance_credits
                  AND ? <= per_order_max_credits
                """,
                (amount, grant_id, amount, amount)
            )
            if cur_grant.rowcount == 0:
                headroom = grant_row["max_allowance_credits"] - (grant_row["spent_credits"] + grant_row["reserved_credits"])
                raise ValueError(f"POLICY_DENIAL: Order amount ({amount}) exceeds remaining grant allowance ({headroom})")

            # 2. Atomic conditional update on buyer wallet
            cur_wallet = c.execute(
                """
                UPDATE accounts
                SET available_credits = available_credits - ?,
                    reserved_credits = reserved_credits + ?
                WHERE account_id = ?
                  AND available_credits >= ?
                """,
                (amount, amount, buyer_owner_id, amount)
            )
            if cur_wallet.rowcount == 0:
                buyer_row = c.execute("SELECT available_credits FROM accounts WHERE account_id = ?", (buyer_owner_id,)).fetchone()
                avail = buyer_row["available_credits"] if buyer_row else 0
                raise ValueError(f"INSUFFICIENT_WALLET_BALANCE: required {amount}, available {avail}")

            # 3. Balanced Journal Entry
            entry = JournalEntry(
                id=generate_uuid("jrn"),
                order_id=order_id,
                operation_type="RESERVATION",
                postings=[
                    LedgerPosting(account_id=buyer_owner_id, account_type="BUYER", amount=-amount, balance_type="AVAILABLE"),
                    LedgerPosting(account_id=buyer_owner_id, account_type="BUYER", amount=amount, balance_type="RESERVED")
                ],
                reason="Purchase order reservation"
            )
            entry.verify_balanced()
            c.execute(
                "INSERT INTO journal (id, order_id, operation_type, postings_json, created_at, reason) VALUES (?, ?, ?, ?, ?, ?)",
                (entry.id, order_id, entry.operation_type, json.dumps([p.model_dump() for p in entry.postings]), entry.created_at, entry.reason)
            )
            return True

    def settle_credits(
        self,
        buyer_owner_id: str,
        seller_id: str,
        grant_id: str,
        buyer_total: int,
        seller_net: int,
        nexus_fee: int,
        order_id: str,
        conn: Optional[sqlite3.Connection] = None
    ) -> bool:
        """
        Atomically settle order: consumes buyer reserved credits, credits seller net and platform fee.
        Consumes grant reservation into permanent spent credits.
        """
        with self._use_conn(conn) as c:
            # 1. Update buyer wallet: deduct reserved credits
            c.execute(
                "UPDATE accounts SET reserved_credits = reserved_credits - ? WHERE account_id = ?",
                (buyer_total, buyer_owner_id)
            )

            # 2. Credit seller wallet
            c.execute(
                """
                INSERT INTO accounts (account_id, account_type, available_credits, reserved_credits)
                VALUES (?, 'SELLER', ?, 0)
                ON CONFLICT(account_id) DO UPDATE SET available_credits = available_credits + ?
                """,
                (seller_id, seller_net, seller_net)
            )

            # 3. Credit platform fee wallet
            c.execute(
                """
                INSERT INTO accounts (account_id, account_type, available_credits, reserved_credits)
                VALUES ('platform_fees', 'PLATFORM_FEES', ?, 0)
                ON CONFLICT(account_id) DO UPDATE SET available_credits = available_credits + ?
                """,
                (nexus_fee, nexus_fee)
            )

            # 4. Update grant: reserved -> spent
            c.execute(
                "UPDATE spend_grants SET reserved_credits = reserved_credits - ?, spent_credits = spent_credits + ? WHERE id = ?",
                (buyer_total, buyer_total, grant_id)
            )

            # 5. Record balanced settlement journal
            entry = JournalEntry(
                id=generate_uuid("jrn"),
                order_id=order_id,
                operation_type="SETTLEMENT",
                postings=[
                    LedgerPosting(account_id=buyer_owner_id, account_type="BUYER", amount=-buyer_total, balance_type="RESERVED"),
                    LedgerPosting(account_id=seller_id, account_type="SELLER", amount=seller_net, balance_type="AVAILABLE"),
                    LedgerPosting(account_id="platform_fees", account_type="PLATFORM_FEES", amount=nexus_fee, balance_type="AVAILABLE")
                ],
                reason="Order successfully delivered and settled"
            )
            entry.verify_balanced()
            c.execute(
                "INSERT INTO journal (id, order_id, operation_type, postings_json, created_at, reason) VALUES (?, ?, ?, ?, ?, ?)",
                (entry.id, order_id, entry.operation_type, json.dumps([p.model_dump() for p in entry.postings]), entry.created_at, entry.reason)
            )
            return True

    def release_credits(
        self,
        buyer_owner_id: str,
        grant_id: str,
        amount: int,
        order_id: str,
        reason: str,
        conn: Optional[sqlite3.Connection] = None
    ) -> bool:
        """
        Atomically release reserved credits back to buyer available balance upon failure, expiry, or cancellation.
        """
        with self._use_conn(conn) as c:
            # 1. Update buyer wallet: reserved -> available
            c.execute(
                "UPDATE accounts SET reserved_credits = reserved_credits - ?, available_credits = available_credits + ? WHERE account_id = ?",
                (amount, amount, buyer_owner_id)
            )

            # 2. Release grant reservation
            c.execute(
                "UPDATE spend_grants SET reserved_credits = reserved_credits - ? WHERE id = ?",
                (amount, grant_id)
            )

            # 3. Record balanced release journal
            entry = JournalEntry(
                id=generate_uuid("jrn"),
                order_id=order_id,
                operation_type="RELEASE",
                postings=[
                    LedgerPosting(account_id=buyer_owner_id, account_type="BUYER", amount=-amount, balance_type="RESERVED"),
                    LedgerPosting(account_id=buyer_owner_id, account_type="BUYER", amount=amount, balance_type="AVAILABLE")
                ],
                reason=f"Reservation release: {reason}"
            )
            entry.verify_balanced()
            c.execute(
                "INSERT INTO journal (id, order_id, operation_type, postings_json, created_at, reason) VALUES (?, ?, ?, ?, ?, ?)",
                (entry.id, order_id, entry.operation_type, json.dumps([p.model_dump() for p in entry.postings]), entry.created_at, entry.reason)
            )
            return True

    def reverse_credits(
        self,
        buyer_owner_id: str,
        seller_id: str,
        grant_id: str,
        buyer_total: int,
        seller_net: int,
        nexus_fee: int,
        order_id: str,
        reason: str,
        conn: Optional[sqlite3.Connection] = None
    ) -> bool:
        """
        Atomically reverse a settled charge upon operator dispute approval.
        Debits seller net and platform fee, credits buyer available, decrements grant spent (F06).
        """
        with self._use_conn(conn) as c:
            # 1. Debit seller wallet
            c.execute(
                "UPDATE accounts SET available_credits = available_credits - ? WHERE account_id = ?",
                (seller_net, seller_id)
            )

            # 2. Debit platform fee wallet
            c.execute(
                "UPDATE accounts SET available_credits = available_credits - ? WHERE account_id = 'platform_fees'",
                (nexus_fee,)
            )

            # 3. Credit buyer wallet: available credits restored
            c.execute(
                "UPDATE accounts SET available_credits = available_credits + ? WHERE account_id = ?",
                (buyer_total, buyer_owner_id)
            )

            # 4. Restore grant spent credits
            c.execute(
                "UPDATE spend_grants SET spent_credits = spent_credits - ? WHERE id = ?",
                (buyer_total, grant_id)
            )

            # 5. Record balanced reversal journal
            entry = JournalEntry(
                id=generate_uuid("jrn"),
                order_id=order_id,
                operation_type="REVERSAL",
                postings=[
                    LedgerPosting(account_id=seller_id, account_type="SELLER", amount=-seller_net, balance_type="AVAILABLE"),
                    LedgerPosting(account_id="platform_fees", account_type="PLATFORM_FEES", amount=-nexus_fee, balance_type="AVAILABLE"),
                    LedgerPosting(account_id=buyer_owner_id, account_type="BUYER", amount=buyer_total, balance_type="AVAILABLE")
                ],
                reason=f"Operator dispute refund reversal: {reason}"
            )
            entry.verify_balanced()
            c.execute(
                "INSERT INTO journal (id, order_id, operation_type, postings_json, created_at, reason) VALUES (?, ?, ?, ?, ?, ?)",
                (entry.id, order_id, entry.operation_type, json.dumps([p.model_dump() for p in entry.postings]), entry.created_at, entry.reason)
            )
            return True
