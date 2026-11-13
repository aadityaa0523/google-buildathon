"""
Nexus Offer and Seller Management Service
"""

from typing import List, Optional, Union
from app.models.core import generate_uuid, utc_now_iso
from app.models.offers import Offer, OfferPricing, SellerProfile, PublicOffer
from app.core.security import validate_seller_endpoint_url
from app.core.database import Database


class OfferService:
    def __init__(self, db: Database, allow_localhost_endpoints: bool = True):
        self.db = db
        self.allow_localhost = allow_localhost_endpoints

    def register_seller(self, owner_id: str, name: str) -> SellerProfile:
        seller_id = generate_uuid("sel")
        profile = SellerProfile(id=seller_id, name=name, owner_id=owner_id, verified_endpoint=True, created_at=utc_now_iso())
        with self.db.transaction() as conn:
            conn.execute(
                "INSERT INTO sellers (id, name, owner_id, verified_endpoint, created_at) VALUES (?, ?, ?, ?, ?)",
                (profile.id, profile.name, profile.owner_id, int(profile.verified_endpoint), profile.created_at)
            )
        return profile

    def publish_offer(
        self,
        seller_id: str,
        title: str,
        description: str,
        buyer_total_credits: int,
        seller_net_credits: int,
        nexus_fee_credits: int,
        execution_deadline_seconds: int = 30,
        endpoint_url: str = "http://localhost:8000/mock_seller",
        endpoint_secret: str = "sec_seller_mock_key_01"
    ) -> Offer:
        # Validate SSRF
        is_valid, msg = validate_seller_endpoint_url(endpoint_url, allow_localhost_for_tests=self.allow_localhost)
        if not is_valid:
            raise ValueError(f"SSRF_VALIDATION_FAILED: {msg}")

        pricing = OfferPricing(
            buyer_total_credits=buyer_total_credits,
            seller_net_credits=seller_net_credits,
            nexus_fee_credits=nexus_fee_credits
        )

        offer_id = generate_uuid("ofr")
        offer = Offer(
            id=offer_id,
            seller_id=seller_id,
            capability_id="invoice.extract.v1",
            version=1,
            title=title,
            description=description,
            pricing=pricing,
            execution_deadline_seconds=execution_deadline_seconds,
            endpoint_url=endpoint_url,
            endpoint_secret=endpoint_secret,
            is_active=True,
            created_at=utc_now_iso()
        )

        with self.db.transaction() as conn:
            conn.execute(
                """
                INSERT INTO offers (id, seller_id, capability_id, version, title, description,
                                    buyer_total_credits, seller_net_credits, nexus_fee_credits,
                                    execution_deadline_seconds, endpoint_url, endpoint_secret,
                                    is_active, created_at, total_completed_orders, p95_latency_ms,
                                    success_rate_pct, average_rating, rating_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (offer.id, offer.seller_id, offer.capability_id, offer.version, offer.title, offer.description,
                 offer.pricing.buyer_total_credits, offer.pricing.seller_net_credits, offer.pricing.nexus_fee_credits,
                 offer.execution_deadline_seconds, offer.endpoint_url, offer.endpoint_secret,
                 int(offer.is_active), offer.created_at, offer.total_completed_orders, offer.p95_latency_ms,
                 offer.success_rate_pct, offer.average_rating, offer.rating_count)
            )
        return offer

    def get_offer(self, offer_id: str) -> Optional[Offer]:
        """Internal retrieval with full dispatch credentials."""
        with self.db.transaction() as conn:
            row = conn.execute("SELECT * FROM offers WHERE id = ?", (offer_id,)).fetchone()
            if not row:
                return None
            data = dict(row)
            data["pricing"] = OfferPricing(
                buyer_total_credits=data["buyer_total_credits"],
                seller_net_credits=data["seller_net_credits"],
                nexus_fee_credits=data["nexus_fee_credits"]
            )
            data["is_active"] = bool(data["is_active"])
            return Offer(**data)

    def get_public_offer(self, offer_id: str) -> Optional[PublicOffer]:
        """Public retrieval omitting sensitive secrets (F02)."""
        offer = self.get_offer(offer_id)
        return offer.to_public() if offer else None

    def search_offers(
        self,
        capability_id: str = "invoice.extract.v1",
        max_buyer_price: Optional[int] = None,
        sort_by: str = "price_asc",
        public_view: bool = True
    ) -> List[Union[PublicOffer, Offer]]:
        """Search and compare transparent seller offers. Defaults to PublicOffer (no secrets)."""
        with self.db.transaction() as conn:
            query = "SELECT * FROM offers WHERE capability_id = ? AND is_active = 1"
            params = [capability_id]
            if max_buyer_price is not None:
                query += " AND buyer_total_credits <= ?"
                params.append(max_buyer_price)

            if sort_by == "price_asc":
                query += " ORDER BY buyer_total_credits ASC"
            elif sort_by == "rating_desc":
                query += " ORDER BY average_rating DESC"
            elif sort_by == "latency_asc":
                query += " ORDER BY p95_latency_ms ASC"

            rows = conn.execute(query, params).fetchall()
            offers = []
            for r in rows:
                data = dict(r)
                data["pricing"] = OfferPricing(
                    buyer_total_credits=data["buyer_total_credits"],
                    seller_net_credits=data["seller_net_credits"],
                    nexus_fee_credits=data["nexus_fee_credits"]
                )
                data["is_active"] = bool(data["is_active"])
                full_offer = Offer(**data)
                offers.append(full_offer.to_public() if public_view else full_offer)
            return offers

    def record_execution_metric(self, offer_id: str, latency_ms: int, is_success: bool):
        """Update live performance metrics based on verified order completions."""
        with self.db.transaction() as conn:
            row = conn.execute("SELECT total_completed_orders, p95_latency_ms, success_rate_pct FROM offers WHERE id = ?", (offer_id,)).fetchone()
            if not row:
                return
            n = row["total_completed_orders"] + 1
            # Running average latency estimation
            new_p95 = int((row["p95_latency_ms"] * 0.9) + (latency_ms * 0.1))
            # Running success rate
            prev_success_count = (row["success_rate_pct"] / 100.0) * row["total_completed_orders"]
            new_success_count = prev_success_count + (1 if is_success else 0)
            new_success_rate = round((new_success_count / n) * 100.0, 1)

            conn.execute(
                "UPDATE offers SET total_completed_orders = ?, p95_latency_ms = ?, success_rate_pct = ? WHERE id = ?",
                (n, new_p95, new_success_rate, offer_id)
            )

