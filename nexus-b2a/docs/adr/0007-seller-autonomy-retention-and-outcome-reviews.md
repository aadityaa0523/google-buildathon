# Separate contract breaches from dissatisfaction and record work reviews

Accepted during the design interview. Seller agents may publish and update offers within their human owner's permissions. Nexus validates changes and versions offers. Existing orders keep their locked terms; pausing an offer stops new purchases without cancelling accepted obligations.

The initial prototype uses synthetic documents. Nexus inputs and outputs expire 24 hours after the order becomes terminal, with that window disclosed before purchase. Transaction metadata is stored separately without document contents. Sellers disclose retention and permitted data use before purchase; Nexus distinguishes its own deletion controls from seller commitments it cannot independently verify. The dispute/evidence window and metadata retention duration remain open.

A broken agreement or failure to complete the contracted task warrants a refund. Dissatisfaction when the agreement was fulfilled can instead be expressed in a work review forming part of the seller profile. Automated validation passing does not immunize a seller from an established contract breach discovered later. Post-settlement breach claims use the previously agreed human review path rather than an LLM-only payment decision. An approved refund is a separate recorded reversal including the commission reversal.

This refines ADR-0004 and ADR-0006: automatic checks determine initial contract-valid delivery but do not prove all promised performance or semantic accuracy. Review eligibility, rating presentation, dispute evidence handling, and the exact first extraction contract remain undecided.
