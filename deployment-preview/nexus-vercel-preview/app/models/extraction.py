"""
Nexus Capability Contract: invoice.extract.v1
Defines strict Pydantic v2 schemas for plain invoice text to structured JSON extraction.
"""

from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field, field_validator, ConfigDict


class EvidenceSpan(BaseModel):
    """
    Pointer to exact character offsets within the original input text.
    Start and end offsets are zero-indexed Unicode code-point positions.
    """
    model_config = ConfigDict(extra="forbid")

    field_name: str = Field(..., description="Target extracted field name (e.g. 'vendor_name', 'total_amount_minor')")
    start_offset: int = Field(..., ge=0, description="Start character index (inclusive)")
    end_offset: int = Field(..., ge=0, description="End character index (exclusive)")
    snippet: str = Field(..., description="Exact substring slice from input text")


class LineItem(BaseModel):
    """Extracted line item from invoice."""
    model_config = ConfigDict(extra="forbid")

    description: str = Field(..., min_length=1, max_length=500)
    quantity: float = Field(..., gt=0, description="Quantity of items")
    unit_price_minor: Optional[int] = Field(None, ge=0, description="Unit price in integer minor units (e.g. paise/cents)")
    total_price_minor: int = Field(..., ge=0, description="Line total in integer minor units")


class ExtractionResult(BaseModel):
    """
    Standardized payload returned by any seller implementing invoice.extract.v1.
    All monetary amounts are represented as integer minor units (e.g., ₹100.50 -> 10050 paise).
    Strict contract: unknown extra fields are forbidden (F07).
    """
    model_config = ConfigDict(extra="forbid")

    contract_version: Literal["invoice.extract.v1"] = "invoice.extract.v1"
    vendor_name: Optional[str] = Field(None, description="Name of the billing company/vendor")
    invoice_number: Optional[str] = Field(None, description="Unique invoice or bill identifier")
    invoice_date: Optional[str] = Field(None, pattern=r"^\d{4}-\d{2}-\d{2}$", description="ISO 8601 date YYYY-MM-DD")
    currency: str = Field(..., min_length=3, max_length=3, description="ISO 4217 3-letter currency code, e.g., INR, USD")
    
    subtotal_amount_minor: Optional[int] = Field(None, ge=0, description="Subtotal amount before taxes")
    tax_amount_minor: Optional[int] = Field(None, ge=0, description="Tax/GST/VAT amount")
    total_amount_minor: int = Field(..., ge=0, description="Total payable amount in minor units")
    
    line_items: List[LineItem] = Field(default_factory=list, description="Extracted invoice line items")
    evidence_spans: List[EvidenceSpan] = Field(default_factory=list, description="Grounding evidence spans into original text")
    
    missing_fields_reasons: Dict[str, str] = Field(
        default_factory=dict, 
        description="Declared reasons for omitted optional fields (e.g. {'tax_amount_minor': 'NOT_MENTIONED_IN_INVOICE'})"
    )

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, v: str) -> str:
        return v.upper()


class ExtractionInput(BaseModel):
    """
    Standardized input payload provided to seller for invoice.extract.v1.
    Strict bounds: Max 10,000 Unicode code points, max 32 KB UTF-8.
    """
    model_config = ConfigDict(extra="forbid")

    raw_text: str = Field(..., min_length=10, max_length=10000, description="Raw plain invoice text")

    @field_validator("raw_text")
    @classmethod
    def validate_byte_limit(cls, v: str) -> str:
        # Enforce maximum 32 KB raw byte size (F08)
        if len(v.encode("utf-8")) > 32768:
            raise ValueError("Raw text exceeds maximum byte limit of 32 KB (32,768 bytes)")
        return v


def validate_extraction_evidence(raw_text: str, result: ExtractionResult) -> List[str]:
    """
    Deterministically verifies that all reported evidence spans match the exact slice of raw_text,
    and that required scalar fields have corresponding evidence spans (F07).
    """
    errors = []
    text_len = len(raw_text)
    span_map = {}

    for span in result.evidence_spans:
        if span.start_offset < 0 or span.end_offset > text_len or span.start_offset >= span.end_offset:
            errors.append(f"INVALID_OFFSETS: [{span.start_offset}:{span.end_offset}] for field '{span.field_name}'")
            continue
        actual_slice = raw_text[span.start_offset:span.end_offset]
        if actual_slice != span.snippet:
            errors.append(
                f"Evidence mismatch (EVIDENCE_MISMATCH): field '{span.field_name}' reported '{span.snippet}', actual text is '{actual_slice}'"
            )
        else:
            span_map[span.field_name] = span

    # Enforce evidence presence for extracted scalar fields
    required_grounded_fields = [
        ("total_amount_minor", result.total_amount_minor),
    ]
    if result.vendor_name:
        required_grounded_fields.append(("vendor_name", result.vendor_name))
    if result.invoice_number:
        required_grounded_fields.append(("invoice_number", result.invoice_number))
    if result.invoice_date:
        required_grounded_fields.append(("invoice_date", result.invoice_date))

    for field_name, val in required_grounded_fields:
        if val is not None and field_name not in span_map:
            errors.append(f"MISSING_EVIDENCE_FOR_FIELD: Extracted field '{field_name}' must have a valid evidence span")

    # Enforce declared reasons for omitted optional fields
    for optional_field in ["subtotal_amount_minor", "tax_amount_minor"]:
        if getattr(result, optional_field) is None and optional_field not in result.missing_fields_reasons:
            errors.append(f"MISSING_FIELD_UNDECLARED: Omitted optional field '{optional_field}' must be declared in missing_fields_reasons")

    # Arithmetic consistency
    if result.subtotal_amount_minor is not None and result.tax_amount_minor is not None:
        if (result.subtotal_amount_minor + result.tax_amount_minor) != result.total_amount_minor:
            errors.append(
                f"ARITHMETIC_MISMATCH: subtotal ({result.subtotal_amount_minor}) + tax ({result.tax_amount_minor}) != total ({result.total_amount_minor})"
            )

    return errors

