# Tie reviews to orders and preserve bounded dispute evidence

Accepted during the design interview. An order that reached execution permits one editable buyer review, including when the order was refunded. Seller profiles show ratings, review counts, and transaction outcomes together. Known common-owner self-dealing reviews are excluded from reputation scores. Subjective reviews and measured performance are presented separately. These controls do not establish that all undisclosed coordinated manipulation can be detected.

Disputes may be opened within 24 hours of an order's terminal execution outcome. Opening a dispute permits preserving only the necessary evidence for up to seven additional days, then deleting it. This exception is disclosed before purchase. Undisputed jobs keep the original 24-hour input/output deletion rule. This explicitly amends ADR-0007; a dispute or review does not silently restart the normal retention clock.

Before dispatch, buyer cancellation releases the order's reserved test credits. After dispatch, cancellation is a request rather than an automatic refund: the seller can acknowledge cancellation, otherwise the original delivery terms continue to apply. Nexus resolves cancellation, expiry, and settlement races to a single recorded financial outcome. A later approved refund is a separate reversal rather than rewriting that outcome.
