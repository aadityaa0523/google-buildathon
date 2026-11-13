"""
Nexus Reference Seller 2: Gemini 2.0 Multimodal/Text Extraction Seller
Uses the official google-genai SDK to parse unstructured invoice text into invoice.extract.v1.
"""

import os
from typing import Dict, Any
from app.models.extraction import ExtractionResult
from app.sellers.deterministic_seller import extract_with_rules


def gemini_seller_handler(job_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes real LLM invoice extraction if GEMINI_API_KEY is present;
    otherwise falls back cleanly to deterministic rule extractor.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    raw_text = job_payload["input_text"]

    if not api_key:
        # Graceful local fallback for offline development & tests
        return extract_with_rules(raw_text)

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        prompt = (
            "You are a strict data extraction service implementing contract 'invoice.extract.v1'.\n"
            "Extract all invoice metadata, line items, and exact evidence spans.\n"
            "All monetary values must be converted to integer minor units (paise/cents, e.g. 100.50 -> 10050).\n"
            "Include start_offset and end_offset matching exact character indices in the input text.\n\n"
            f"INPUT INVOICE TEXT:\n{raw_text}"
        )

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ExtractionResult,
                temperature=0.0
            )
        )
        return ExtractionResult.model_validate_json(response.text).model_dump()
    except Exception:
        # Fallback to rule engine if API call fails or quota exceeded
        return extract_with_rules(raw_text)

