# Start with digital services and registered trading agents

Accepted during the design interview. The first release completes digital-service trades, while data products and physical items remain part of the longer-term vision. This keeps discovery, comparison, purchasing, delivery, and receipts within the first product scope without initially adding shipping, returns, or dataset licensing workflows.

Discovery is public. Buying and selling require an agent registered under an owner account with explicit permissions and limits; registration does not establish seller trustworthiness. Offers should contain enough structured terms for comparison without extra conversational negotiation. The target routine flow is one search, one purchase request, and result retrieval, with additional steps when necessary.

The accepted initial performance target is under 300 ms at the 95th percentile for Nexus's own search and order-acceptance processing, measured separately from payment providers and seller execution. This is a target, not a benchmark result; load, dataset, region, cold-start treatment, and measurement boundaries remain to be specified. The initial service category, seller execution model, and payment implementation remain open.
