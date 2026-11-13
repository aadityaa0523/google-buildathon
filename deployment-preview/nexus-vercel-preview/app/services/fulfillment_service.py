"""
Nexus Fulfillment Service
Dispatches paid jobs to seller endpoints, verifies HMAC signatures, and validates invoice.extract.v1 results.
"""

import hmac
import hashlib
import json
from typing import Dict, Any, Tuple, Optional
import httpx

from app.models.orders import Order
from app.models.offers import Offer
from app.models.extraction import ExtractionInput, ExtractionResult, validate_extraction_evidence


def compute_hmac_signature(payload_bytes: bytes, secret: str) -> str:
    """Compute HMAC-SHA256 signature for webhook verification."""
    return hmac.new(secret.encode("utf-8"), payload_bytes, hashlib.sha256).hexdigest()


class FulfillmentService:
    def __init__(self, http_client: Optional[httpx.Client] = None):
        self.client = http_client or httpx.Client(timeout=10.0)
        self.mock_seller_handlers: Dict[str, Any] = {}

    def register_mock_seller(self, endpoint_url: str, handler_func):
        """Allows registering in-memory seller handlers for instant local test runs."""
        self.mock_seller_handlers[endpoint_url] = handler_func

    def dispatch_job(self, order: Order, offer: Offer, raw_input_text: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
        """
        Dispatches job to seller endpoint.
        Returns: (success, result_dict_or_none, error_message_or_none)
        """
        job_payload = {
            "job_id": order.seller_job_id,
            "order_id": order.id,
            "capability_id": "invoice.extract.v1",
            "input_text": raw_input_text,
            "deadline_at": order.deadline_at
        }
        payload_bytes = json.dumps(job_payload, sort_keys=True).encode("utf-8")
        signature = compute_hmac_signature(payload_bytes, offer.endpoint_secret)

        # 1. Check if mock handler is registered (for tests)
        if offer.endpoint_url in self.mock_seller_handlers:
            handler = self.mock_seller_handlers[offer.endpoint_url]
            try:
                result_data = handler(job_payload)
                return True, result_data, None
            except Exception as e:
                return False, None, str(e)

        # 2. Real HTTP dispatch
        headers = {
            "Content-Type": "application/json",
            "X-Nexus-Signature": signature,
            "X-Nexus-Job-ID": order.seller_job_id or order.id
        }
        try:
            resp = self.client.post(offer.endpoint_url, content=payload_bytes, headers=headers)
            if resp.status_code != 200:
                return False, None, f"SELLER_HTTP_ERROR_{resp.status_code}: {resp.text[:200]}"
            return True, resp.json(), None
        except httpx.TimeoutException:
            return False, None, "SELLER_TIMEOUT"
        except Exception as e:
            return False, None, f"SELLER_CONNECTION_ERROR: {str(e)}"

    def validate_extraction_result(self, raw_input_text: str, result_data: Dict[str, Any]) -> Tuple[bool, Optional[ExtractionResult], list[str]]:
        """
        Strict validation of seller extraction result against invoice.extract.v1 specification.
        Returns: (is_valid, parsed_result_or_none, list_of_errors)
        """
        # 1. Schema parsing
        try:
            result = ExtractionResult(**result_data)
        except Exception as e:
            return False, None, [f"SCHEMA_VIOLATION: {str(e)}"]

        # 2. Deterministic evidence span verification
        evidence_errors = validate_extraction_evidence(raw_input_text, result)
        if evidence_errors:
            return False, result, evidence_errors

        # 3. Numeric consistency check
        if result.subtotal_amount_minor is not None and result.tax_amount_minor is not None:
            expected_total = result.subtotal_amount_minor + result.tax_amount_minor
            if expected_total != result.total_amount_minor:
                return False, result, [
                    f"NUMERIC_INCONSISTENCY: subtotal ({result.subtotal_amount_minor}) + tax ({result.tax_amount_minor}) "
                    f"= {expected_total}, but total is {result.total_amount_minor}"
                ]

        return True, result, []

