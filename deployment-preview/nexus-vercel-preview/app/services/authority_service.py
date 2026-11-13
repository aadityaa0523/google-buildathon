"""
Nexus Authority and Credential Service
Handles owner authentication, agent registration, secret hashing, and spend grant lifecycle.
"""

from datetime import datetime, timezone
import json
from typing import Optional, Tuple
from app.models.core import generate_uuid, utc_now_iso
from app.models.authority import Owner, Agent, AgentCredential, OwnerCredential, SpendGrant
from app.core.security import generate_agent_key, generate_owner_key, hash_secret
from app.core.database import Database


def normalize_to_utc_iso(ts_str: Optional[str]) -> Optional[str]:
    """Ensures ISO timestamp is normalized to UTC with standard +00:00 offset (F09)."""
    if not ts_str:
        return None
    try:
        dt = datetime.fromisoformat(ts_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        else:
            dt = dt.astimezone(timezone.utc)
        return dt.isoformat()
    except Exception:
        return ts_str


class AuthorityService:
    def __init__(self, db: Database):
        self.db = db

    def create_owner(self, email: str, name: str) -> Owner:
        with self.db.transaction() as conn:
            row = conn.execute("SELECT * FROM owners WHERE email = ?", (email,)).fetchone()
            if row:
                return Owner(**dict(row))
            owner_id = generate_uuid("usr")
            owner = Owner(id=owner_id, email=email, name=name, created_at=utc_now_iso())
            conn.execute(
                "INSERT INTO owners (id, email, name, created_at) VALUES (?, ?, ?, ?)",
                (owner.id, owner.email, owner.name, owner.created_at)
            )
            return owner

    def get_owner(self, owner_id: str) -> Optional[Owner]:
        with self.db.transaction() as conn:
            row = conn.execute("SELECT * FROM owners WHERE id = ?", (owner_id,)).fetchone()
            return Owner(**dict(row)) if row else None

    def issue_owner_key(self, owner_id: str) -> Tuple[str, OwnerCredential]:
        """
        Issues a new API key for a human owner (F01).
        Returns: (raw_secret_token_shown_once, credential_record)
        """
        with self.db.transaction() as conn:
            owner_row = conn.execute("SELECT * FROM owners WHERE id = ?", (owner_id,)).fetchone()
            if not owner_row:
                raise ValueError("Owner not found")

            raw_token, prefix, hashed = generate_owner_key()
            cred_id = generate_uuid("crd_own")
            cred = OwnerCredential(
                id=cred_id,
                owner_id=owner_id,
                key_prefix=prefix,
                hashed_secret=hashed,
                created_at=utc_now_iso()
            )
            conn.execute(
                "INSERT INTO owner_credentials (id, owner_id, key_prefix, hashed_secret, created_at) VALUES (?, ?, ?, ?, ?)",
                (cred.id, cred.owner_id, cred.key_prefix, cred.hashed_secret, cred.created_at)
            )
            return raw_token, cred

    def authenticate_owner_token(self, raw_token: str) -> Owner:
        """
        Verifies an owner bearer token against hashed credentials (F01).
        Returns: Owner
        """
        hashed = hash_secret(raw_token)
        with self.db.transaction() as conn:
            row = conn.execute(
                """
                SELECT c.revoked_at, o.*
                FROM owner_credentials c
                JOIN owners o ON c.owner_id = o.id
                WHERE c.hashed_secret = ?
                """,
                (hashed,)
            ).fetchone()
            if not row:
                raise ValueError("INVALID_OWNER_CREDENTIALS")
            if row["revoked_at"] is not None:
                raise ValueError("OWNER_CREDENTIAL_REVOKED")

            return Owner(id=row["id"], email=row["email"], name=row["name"], created_at=row["created_at"])

    def register_agent(self, owner_id: str, name: str) -> Agent:
        agent_id = generate_uuid("agt")
        agent = Agent(id=agent_id, owner_id=owner_id, name=name, created_at=utc_now_iso())
        with self.db.transaction() as conn:
            conn.execute(
                "INSERT INTO agents (id, owner_id, name, is_active, created_at) VALUES (?, ?, ?, 1, ?)",
                (agent.id, agent.owner_id, agent.name, agent.created_at)
            )
        return agent

    def issue_agent_key(self, agent_id: str) -> Tuple[str, AgentCredential]:
        """
        Issues a new API key for an agent.
        Returns: (raw_secret_token_shown_once, credential_record)
        """
        with self.db.transaction() as conn:
            agent_row = conn.execute("SELECT owner_id FROM agents WHERE id = ?", (agent_id,)).fetchone()
            if not agent_row:
                raise ValueError("Agent not found")
            owner_id = agent_row["owner_id"]

            raw_token, prefix, hashed = generate_agent_key()
            cred_id = generate_uuid("crd")
            cred = AgentCredential(
                id=cred_id,
                agent_id=agent_id,
                owner_id=owner_id,
                key_prefix=prefix,
                hashed_secret=hashed,
                created_at=utc_now_iso()
            )
            conn.execute(
                "INSERT INTO credentials (id, agent_id, owner_id, key_prefix, hashed_secret, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                (cred.id, cred.agent_id, cred.owner_id, cred.key_prefix, cred.hashed_secret, cred.created_at)
            )
            return raw_token, cred

    def authenticate_agent_token(self, raw_token: str) -> Tuple[Agent, Owner]:
        """
        Verifies a bearer token against hashed credentials.
        Returns: (Agent, Owner)
        """
        hashed = hash_secret(raw_token)
        with self.db.transaction() as conn:
            row = conn.execute(
                """
                SELECT c.revoked_at, a.*, o.email as owner_email, o.name as owner_name
                FROM credentials c
                JOIN agents a ON c.agent_id = a.id
                JOIN owners o ON a.owner_id = o.id
                WHERE c.hashed_secret = ?
                """,
                (hashed,)
            ).fetchone()
            if not row:
                raise ValueError("INVALID_CREDENTIALS")
            if row["revoked_at"] is not None:
                raise ValueError("CREDENTIAL_REVOKED")
            if not row["is_active"]:
                raise ValueError("AGENT_DEACTIVATED")

            agent = Agent(id=row["id"], owner_id=row["owner_id"], name=row["name"], is_active=bool(row["is_active"]))
            owner = Owner(id=row["owner_id"], email=row["owner_email"], name=row["owner_name"])
            return agent, owner

    def create_spend_grant(
        self,
        owner_id: str,
        agent_id: str,
        max_allowance_credits: int,
        per_order_max_credits: int,
        allowed_capabilities: Optional[list[str]] = None,
        expires_at: Optional[str] = None
    ) -> SpendGrant:
        grant_id = generate_uuid("grt")
        caps = allowed_capabilities or ["invoice.extract.v1"]
        normalized_expires_at = normalize_to_utc_iso(expires_at)
        grant = SpendGrant(
            id=grant_id,
            owner_id=owner_id,
            agent_id=agent_id,
            max_allowance_credits=max_allowance_credits,
            per_order_max_credits=per_order_max_credits,
            allowed_capabilities=caps,
            expires_at=normalized_expires_at,
            spent_credits=0,
            reserved_credits=0,
            is_revoked=False
        )
        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT INTO spend_grants (id, owner_id, agent_id, max_allowance_credits, spent_credits, reserved_credits,
                                         per_order_max_credits, allowed_capabilities, expires_at, is_revoked)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (grant.id, grant.owner_id, grant.agent_id, grant.max_allowance_credits, grant.spent_credits, grant.reserved_credits,
                 grant.per_order_max_credits, json.dumps(grant.allowed_capabilities), grant.expires_at, int(grant.is_revoked))
            )
        return grant

    def get_spend_grant(self, grant_id: str) -> Optional[SpendGrant]:
        with self.db.transaction() as conn:
            row = conn.execute("SELECT * FROM spend_grants WHERE id = ?", (grant_id,)).fetchone()
            if not row:
                return None
            data = dict(row)
            data["allowed_capabilities"] = json.loads(data["allowed_capabilities"])
            data["is_revoked"] = bool(data["is_revoked"])
            return SpendGrant(**data)

    def revoke_spend_grant(self, grant_id: str, owner_id: str) -> bool:
        with self.db.transaction() as conn:
            conn.execute("UPDATE spend_grants SET is_revoked = 1 WHERE id = ? AND owner_id = ?", (grant_id, owner_id))
            return True
