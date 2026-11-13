"""
Nexus Reference Seller 1: Fast Deterministic Extractor
Rule-based regex extractor producing exact schema-compliant results with accurate evidence spans.
"""

import re
from typing import Dict, Any, List, Optional
from app.models.extraction import ExtractionResult, LineItem, EvidenceSpan


def extract_with_rules(raw_text: str) -> Dict[str, Any]:
    """
    Deterministically parses plain text invoice and produces strict invoice.extract.v1 output.
    Extracts real vendors, line items, and grand totals with exact character offset evidence spans.
    """
    evidence_spans: List[Dict[str, Any]] = []

    # 1. Vendor Name
    vendor_match = re.search(r"(?:Seller|Vendor|Company|Billed By|From):\s*([A-Za-z0-9\s,\.\-]+?)(?:\n|$)", raw_text, re.IGNORECASE)
    if vendor_match:
        vendor_name = vendor_match.group(1).strip()
        span_start = vendor_match.start(1)
        span_end = vendor_match.end(1)
        evidence_spans.append({
            "field_name": "vendor_name",
            "start_offset": span_start,
            "end_offset": span_end,
            "snippet": raw_text[span_start:span_end]
        })
    else:
        vendor_name = None

    # 2. Invoice Number
    inv_match = re.search(r"\b(?:Invoice\s*(?:No|Number|#)\s*[:\s]*|Invoice\s*:\s*)([A-Za-z0-9\-_]+)", raw_text, re.IGNORECASE)
    if inv_match:
        invoice_number = inv_match.group(1).strip()
        span_start = inv_match.start(1)
        span_end = inv_match.end(1)
        evidence_spans.append({
            "field_name": "invoice_number",
            "start_offset": span_start,
            "end_offset": span_end,
            "snippet": raw_text[span_start:span_end]
        })
    else:
        invoice_number = None

    # 3. Invoice Date (YYYY-MM-DD)
    date_match = re.search(r"\b(?:Date[:\s]*)([0-9]{4}-[0-9]{2}-[0-9]{2})", raw_text, re.IGNORECASE)
    if date_match:
        invoice_date = date_match.group(1).strip()
        span_start = date_match.start(1)
        span_end = date_match.end(1)
        evidence_spans.append({
            "field_name": "invoice_date",
            "start_offset": span_start,
            "end_offset": span_end,
            "snippet": raw_text[span_start:span_end]
        })
    else:
        invoice_date = None

    # 4. Currency
    curr_match = re.search(r"\b(INR|USD|EUR|GBP)\b", raw_text, re.IGNORECASE)
    if curr_match:
        currency = curr_match.group(1).upper()
    elif "₹" in raw_text:
        currency = "INR"
    elif "$" in raw_text:
        currency = "USD"
    else:
        currency = "INR"

    # Helper for parsing amounts
    def parse_amount(val_str: str) -> Optional[int]:
        cleaned = val_str.replace(",", "").strip()
        try:
            return int(round(float(cleaned) * 100))
        except ValueError:
            return None

    # 5. Extract Line Items
    line_items: List[Dict[str, Any]] = []
    item_pattern = re.compile(
        r"(?:^|\n)\s*(?:\d+[\.\)]\s*)?([^\n|]+?)\n\s*Qty:\s*(\d+(?:\.\d+)?)\s*\|\s*Unit Price:\s*(?:₹|\$)?([0-9,]+(?:\.[0-9]{2})?)\s*\|\s*Total:\s*(?:₹|\$)?([0-9,]+(?:\.[0-9]{2})?)",
        re.MULTILINE
    )
    for m in item_pattern.finditer(raw_text):
        desc = m.group(1).strip()
        qty = float(m.group(2))
        unit_minor = parse_amount(m.group(3))
        total_minor = parse_amount(m.group(4)) or 0
        line_items.append({
            "description": desc,
            "quantity": qty,
            "unit_price_minor": unit_minor,
            "total_price_minor": total_minor
        })

    # 6. Subtotal
    sub_match = re.search(r"\b(?:Subtotal|Sub Total)[:\s]*(?:₹|\$)?\s*([0-9,]+(?:\.[0-9]{1,2})?)", raw_text, re.IGNORECASE)
    subtotal_minor = parse_amount(sub_match.group(1)) if sub_match else None

    # 7. Taxes (sum CGST, SGST, IGST, VAT, or general Tax lines)
    tax_pattern = re.compile(r"\b(?:CGST|SGST|IGST|VAT|Tax)(?:\s*\([^)]+\))?[:\s]*(?:₹|\$)?\s*([0-9,]+(?:\.[0-9]{1,2})?)", re.IGNORECASE)
    tax_matches = tax_pattern.findall(raw_text)
    if tax_matches:
        tax_minor = sum(parse_amount(t) or 0 for t in tax_matches)
    else:
        tax_minor = None

    # 8. Grand Total (Prefer explicit Total Amount / Grand Total, then footer Total)
    grand_match = re.search(r"\b(?:Total\s+Amount|Grand\s+Total|Net\s+Payable|Amount\s+Payable)[:\s]*(?:₹|\$)?\s*([0-9,]+(?:\.[0-9]{1,2})?)", raw_text, re.IGNORECASE)
    if not grand_match:
        # Fallback to finding the last "Total:" at end of text (after items)
        all_totals = list(re.finditer(r"\bTotal[:\s]*(?:₹|\$)?\s*([0-9,]+(?:\.[0-9]{1,2})?)", raw_text, re.IGNORECASE))
        grand_match = all_totals[-1] if all_totals else None

    if grand_match:
        total_minor = parse_amount(grand_match.group(1))
        span_start = grand_match.start(1)
        span_end = grand_match.end(1)
        evidence_spans.append({
            "field_name": "total_amount_minor",
            "start_offset": span_start,
            "end_offset": span_end,
            "snippet": raw_text[span_start:span_end]
        })
    else:
        total_minor = (subtotal_minor or 0) + (tax_minor or 0)

    # Missing fields declaration
    missing_reasons = {}
    if subtotal_minor is None:
        missing_reasons["subtotal_amount_minor"] = "NOT_MENTIONED_IN_INVOICE"
    if tax_minor is None:
        missing_reasons["tax_amount_minor"] = "NOT_MENTIONED_IN_INVOICE"
    if vendor_name is None:
        missing_reasons["vendor_name"] = "NOT_MENTIONED_IN_INVOICE"
    if invoice_number is None:
        missing_reasons["invoice_number"] = "NOT_MENTIONED_IN_INVOICE"
    if invoice_date is None:
        missing_reasons["invoice_date"] = "NOT_MENTIONED_IN_INVOICE"

    return {
        "contract_version": "invoice.extract.v1",
        "vendor_name": vendor_name,
        "invoice_number": invoice_number,
        "invoice_date": invoice_date,
        "currency": currency,
        "subtotal_amount_minor": subtotal_minor,
        "tax_amount_minor": tax_minor,
        "total_amount_minor": total_minor or 0,
        "line_items": line_items,
        "evidence_spans": evidence_spans,
        "missing_fields_reasons": missing_reasons
    }


def deterministic_seller_handler(job_payload: Dict[str, Any]) -> Dict[str, Any]:
    """Handler invoked by Nexus fulfillment service."""
    raw_text = job_payload["input_text"]
    return extract_with_rules(raw_text)
