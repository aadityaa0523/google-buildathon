# Enforce order identity and spending authority across HTTP and MCP

Accepted during the design interview. Repeating a purchase identifier with an unchanged request returns the existing order. Reuse with changed inputs is rejected; changed inputs require a new purchase identifier. Seller execution uses a stable job identifier without claiming network retries guarantee exactly-once execution. At the delivery deadline Nexus releases reserved test credits if no contract-valid result was accepted, and late results cannot settle that expired order. Settlement and expiry must resolve atomically to one outcome. Switching sellers requires a new buyer-authorized purchase.

Nexus, not the calling agent, enforces human-owner limits: per-order maximum, aggregate allowance, permitted services, and expiry. Aggregate checks include both spent credits and active reservations across concurrent orders. Revocation stops new purchases; existing orders follow their locked terms.

An authoritative HTTP API provides discovery, purchasing, and results. An MCP adapter exposes the same operations and applies identical authorization and transaction rules. Sellers integrate through an HTTP job contract. Agent-exclusive trading means a machine-first interface; it is not an assertion that Nexus can distinguish AI callers from humans running scripts.
