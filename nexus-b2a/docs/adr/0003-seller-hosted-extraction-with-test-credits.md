# Fulfil extraction jobs through seller-hosted services using test credits

Accepted during the design interview. The first service is text-to-JSON extraction using a shared input/output contract so agents can compare competing sellers. The initial example extracts invoice text into structured data; the exact schema and acceptance rules remain open.

Sellers execute services at their registered endpoints rather than uploading executable code to Nexus. Nexus owns discovery, purchasing, job tracking, and transaction records; sellers own execution. Demonstration sellers run as separate services through the same integration path available to independently registered sellers. This avoids adding a hosted-code execution platform to the initial marketplace.

The first prototype delivers real service outputs while accounting in explicitly labelled test credits. Buyer debits, seller credits, and failure release/refund paths will be exercised without claiming real-money settlement. Live payments are a separate milestone requiring verified provider integration. Pricing, result acceptance, settlement timing, data handling, and failure semantics are not settled by this decision.
