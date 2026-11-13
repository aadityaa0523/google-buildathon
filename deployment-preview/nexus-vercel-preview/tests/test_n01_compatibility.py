"""
Tests for Milestone M0: N01 Compatibility Spike and N03 Extraction Contract
"""

from app.models.extraction import ExtractionInput, ExtractionResult, validate_extraction_evidence
from app.sellers.deterministic_seller import extract_with_rules
from tests.conftest import SAMPLE_INVOICE_TEXT


def test_n01_extraction_contract_schema_and_evidence():
    """Verify that extraction contract invoice.extract.v1 parses and validates evidence spans."""
    # 1. Validate Input bounds
    input_obj = ExtractionInput(raw_text=SAMPLE_INVOICE_TEXT)
    assert len(input_obj.raw_text) > 10

    # 2. Run deterministic extraction
    output_dict = extract_with_rules(input_obj.raw_text)

    # 3. Parse with strict Pydantic model
    result = ExtractionResult(**output_dict)
    assert result.contract_version == "invoice.extract.v1"
    assert result.vendor_name == "Acme Industrial Supplies Ltd"
    assert result.invoice_number == "INV-2026-8841"
    assert result.invoice_date == "2026-11-14"
    assert result.currency == "INR"
    assert result.subtotal_amount_minor == 1000000
    assert result.tax_amount_minor == 180000
    assert result.total_amount_minor == 1180000

    # 4. Verify evidence spans match exact slices of text
    errors = validate_extraction_evidence(input_obj.raw_text, result)
    assert errors == [], f"Evidence errors encountered: {errors}"
    assert len(result.evidence_spans) >= 3


def test_n03_extraction_negative_evidence_detection():
    """Verify that fabricated or corrupt evidence offsets are deterministically caught."""
    output_dict = extract_with_rules(SAMPLE_INVOICE_TEXT)
    # Corrupt snippet
    output_dict["evidence_spans"][0]["snippet"] = "Wrong Nonexistent Snippet"
    result = ExtractionResult(**output_dict)

    errors = validate_extraction_evidence(SAMPLE_INVOICE_TEXT, result)
    assert len(errors) > 0
    assert "Evidence mismatch" in errors[0]

