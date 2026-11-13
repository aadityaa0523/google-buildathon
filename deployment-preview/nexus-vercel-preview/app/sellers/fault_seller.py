"""
Nexus Reference Seller 3: Fault-Injecting Seller
Controllable mock seller that injects timeouts, schema corruptions, and invalid evidence.
"""

import time
from typing import Dict, Any

FAULT_MODE_NONE = "NONE"
FAULT_MODE_TIMEOUT = "TIMEOUT"
FAULT_MODE_SCHEMA_ERROR = "SCHEMA_ERROR"
FAULT_MODE_BAD_EVIDENCE = "BAD_EVIDENCE"
FAULT_MODE_NUMERIC_ERROR = "NUMERIC_ERROR"
FAULT_MODE_INTERNAL_ERROR = "INTERNAL_ERROR"

current_fault_mode = FAULT_MODE_NONE


def set_fault_mode(mode: str):
    global current_fault_mode
    current_fault_mode = mode


def fault_seller_handler(job_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Controllable seller handler simulating network and schema failures."""
    from app.sellers.deterministic_seller import extract_with_rules

    if current_fault_mode == FAULT_MODE_TIMEOUT:
        time.sleep(1.0)
        raise TimeoutError("Seller timed out after execution window")

    if current_fault_mode == FAULT_MODE_INTERNAL_ERROR:
        raise RuntimeError("SELLER_INTERNAL_CRASH: Unhandled database exception")

    base_result = extract_with_rules(job_payload["input_text"])

    if current_fault_mode == FAULT_MODE_SCHEMA_ERROR:
        # Delete required total_amount_minor to trigger schema violation
        del base_result["total_amount_minor"]
        return base_result

    if current_fault_mode == FAULT_MODE_BAD_EVIDENCE:
        # Corrupt evidence snippet to trigger evidence mismatch error
        if base_result["evidence_spans"]:
            base_result["evidence_spans"][0]["snippet"] = "Completely Fabricated Text Not In Invoice"
        return base_result

    if current_fault_mode == FAULT_MODE_NUMERIC_ERROR:
        # Force subtotal + tax != total
        base_result["subtotal_amount_minor"] = 50000
        base_result["tax_amount_minor"] = 10000
        base_result["total_amount_minor"] = 99999
        return base_result

    return base_result

