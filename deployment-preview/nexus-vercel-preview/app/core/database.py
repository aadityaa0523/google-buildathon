"""
Nexus Durable Database Storage Layer
Provides ACID transactional storage across all commerce, authority, and accounting records.
"""

import sqlite3
import tempfile
import json
from contextlib import contextmanager
from typing import Optional, List, Dict, Any
from pathlib import Path


class Database:
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self._mem_conn = None
        if db_path == ":memory:":
            self._mem_conn = sqlite3.connect(":memory:", check_same_thread=False)
            self._mem_conn.row_factory = sqlite3.Row
            self._mem_conn.execute("PRAGMA foreign_keys=ON")
        self._init_schema()

    def get_connection(self) -> sqlite3.Connection:
        if self._mem_conn is not None:
            return self._mem_conn
        conn = sqlite3.connect(self.db_path, timeout=10.0, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    @contextmanager
    def transaction(self):
        conn = self.get_connection()
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            if self._mem_conn is None:
                conn.close()

    def _init_schema(self):
        with self.transaction() as conn:
            conn.executescript("""
            CREATE TABLE IF NOT EXISTS owners (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                owner_id TEXT NOT NULL,
                name TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                FOREIGN KEY (owner_id) REFERENCES owners(id)
            );

            CREATE TABLE IF NOT EXISTS credentials (
                id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                owner_id TEXT NOT NULL,
                key_prefix TEXT NOT NULL,
                hashed_secret TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL,
                revoked_at TEXT,
                FOREIGN KEY (agent_id) REFERENCES agents(id),
                FOREIGN KEY (owner_id) REFERENCES owners(id)
            );

            CREATE TABLE IF NOT EXISTS owner_credentials (
                id TEXT PRIMARY KEY,
                owner_id TEXT NOT NULL,
                key_prefix TEXT NOT NULL,
                hashed_secret TEXT UNIQUE NOT NULL,
                created_at TEXT NOT NULL,
                revoked_at TEXT,
                FOREIGN KEY (owner_id) REFERENCES owners(id)
            );

            CREATE TABLE IF NOT EXISTS spend_grants (
                id TEXT PRIMARY KEY,
                owner_id TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                max_allowance_credits INTEGER NOT NULL,
                spent_credits INTEGER NOT NULL DEFAULT 0,
                reserved_credits INTEGER NOT NULL DEFAULT 0,
                per_order_max_credits INTEGER NOT NULL,
                allowed_capabilities TEXT NOT NULL, -- JSON list
                expires_at TEXT,
                is_revoked INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (owner_id) REFERENCES owners(id),
                FOREIGN KEY (agent_id) REFERENCES agents(id)
            );

            CREATE TABLE IF NOT EXISTS accounts (
                account_id TEXT PRIMARY KEY,
                account_type TEXT NOT NULL,
                available_credits INTEGER NOT NULL DEFAULT 0,
                reserved_credits INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS sellers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                owner_id TEXT NOT NULL,
                verified_endpoint INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                FOREIGN KEY (owner_id) REFERENCES owners(id)
            );

            CREATE TABLE IF NOT EXISTS offers (
                id TEXT PRIMARY KEY,
                seller_id TEXT NOT NULL,
                capability_id TEXT NOT NULL,
                version INTEGER NOT NULL DEFAULT 1,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                buyer_total_credits INTEGER NOT NULL,
                seller_net_credits INTEGER NOT NULL,
                nexus_fee_credits INTEGER NOT NULL,
                execution_deadline_seconds INTEGER NOT NULL,
                endpoint_url TEXT NOT NULL,
                endpoint_secret TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL,
                total_completed_orders INTEGER NOT NULL DEFAULT 0,
                p95_latency_ms INTEGER NOT NULL DEFAULT 1200,
                success_rate_pct REAL NOT NULL DEFAULT 100.0,
                average_rating REAL NOT NULL DEFAULT 0.0,
                rating_count INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (seller_id) REFERENCES sellers(id)
            );

            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                buyer_owner_id TEXT NOT NULL,
                buyer_agent_id TEXT NOT NULL,
                spend_grant_id TEXT NOT NULL,
                seller_id TEXT NOT NULL,
                offer_id TEXT NOT NULL,
                offer_version INTEGER NOT NULL,
                terms_hash TEXT NOT NULL,
                buyer_total_credits INTEGER NOT NULL,
                seller_net_credits INTEGER NOT NULL,
                nexus_fee_credits INTEGER NOT NULL,
                execution_state TEXT NOT NULL,
                accounting_state TEXT NOT NULL,
                idempotency_key TEXT NOT NULL,
                request_hash TEXT NOT NULL,
                input_text_id TEXT NOT NULL,
                result_payload_id TEXT,
                created_at TEXT NOT NULL,
                deadline_at TEXT NOT NULL,
                terminal_at TEXT,
                accessible_until TEXT,
                dispatch_attempts INTEGER NOT NULL DEFAULT 0,
                seller_job_id TEXT,
                error_code TEXT,
                error_message TEXT,
                validation_errors TEXT, -- JSON list
                FOREIGN KEY (spend_grant_id) REFERENCES spend_grants(id),
                FOREIGN KEY (seller_id) REFERENCES sellers(id),
                FOREIGN KEY (offer_id) REFERENCES offers(id)
            );

            CREATE TABLE IF NOT EXISTS payloads (
                id TEXT PRIMARY KEY,
                order_id TEXT NOT NULL,
                payload_type TEXT NOT NULL,
                content_text TEXT NOT NULL,
                accessible_until TEXT NOT NULL,
                is_deleted INTEGER NOT NULL DEFAULT 0,
                dispute_hold_until TEXT
            );

            CREATE TABLE IF NOT EXISTS journal (
                id TEXT PRIMARY KEY,
                order_id TEXT,
                operation_type TEXT NOT NULL,
                postings_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                reason TEXT
            );

            CREATE TABLE IF NOT EXISTS reviews (
                id TEXT PRIMARY KEY,
                order_id TEXT UNIQUE NOT NULL,
                buyer_owner_id TEXT NOT NULL,
                seller_id TEXT NOT NULL,
                rating INTEGER NOT NULL,
                comment TEXT NOT NULL,
                is_common_owner INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            );

            CREATE TABLE IF NOT EXISTS disputes (
                id TEXT PRIMARY KEY,
                order_id TEXT UNIQUE NOT NULL,
                buyer_owner_id TEXT NOT NULL,
                seller_id TEXT NOT NULL,
                reason TEXT NOT NULL,
                details TEXT NOT NULL,
                status TEXT NOT NULL,
                evidence_hold_until TEXT NOT NULL,
                created_at TEXT NOT NULL,
                resolved_at TEXT,
                operator_reason TEXT,
                FOREIGN KEY (order_id) REFERENCES orders(id)
            );

            CREATE TABLE IF NOT EXISTS outbox (
                id TEXT PRIMARY KEY,
                order_id TEXT NOT NULL,
                status TEXT NOT NULL, -- PENDING, CLAIMED, COMPLETED, FAILED
                attempts INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                claimed_at TEXT,
                completed_at TEXT
            );

            CREATE TABLE IF NOT EXISTS idempotency_records (
                idempotency_key TEXT NOT NULL,
                agent_id TEXT NOT NULL,
                request_hash TEXT NOT NULL,
                order_id TEXT NOT NULL,
                created_at TEXT NOT NULL,
                PRIMARY KEY (idempotency_key, agent_id)
            );
            """)


# Global default database instance (using SQLite file nexus_dev.db)
default_db_path = str(Path(tempfile.gettempdir()) / "nexus_preview.db")
global_db = Database(default_db_path)
