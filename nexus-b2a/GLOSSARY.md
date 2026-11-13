# Nexus-B2A

Nexus-B2A is an agent-native marketplace focused initially on SaaS capabilities. Services, data, and physical items remain part of its broader vision; industrial procurement was an illustrative example.

## Language

**Nexus marketplace**:
The venue where agents discover competing sellers, compare offers, and purchase services, data, or physical items.
_Avoid_: Supplier gateway (when referring to the whole product)

**Structured offer**:
A seller's offer expressed as explicit terms that an agent can compare and accept without a conversational negotiation.

**SaaS capability**:
A software operation supplied by a seller, with declared inputs, outputs, and commercial terms, such as extracting invoice text into structured data.
_Avoid_: Subscription (when referring to a single operation)

**Order**:
A buyer-authorized purchase from a selected seller under locked terms, with a persistent identity used for status, result retrieval, reviews, and disputes.

**Test credits**:
Nonredeemable units used to demonstrate Nexus purchasing and accounting without moving money.
_Avoid_: Revenue, cash, withdrawable balance

**Reservation**:
The portion of a buyer's test-credit balance and spending allowance committed to an accepted order while its outcome is pending.

**Settlement**:
The recorded allocation of an order's reserved charge to seller proceeds and Nexus commission after contract-valid delivery.

**Release**:
The return of an unsettled order's reservation to the buyer when it fails, expires, or is cancelled under its terms.
_Avoid_: Refund (when no settlement occurred)

**Refund**:
A recorded reversal of a settled charge following an approved contract-breach decision, including reversal of the corresponding commission.
_Avoid_: Release

**Work review**:
An editable buyer assessment linked to an order that reached execution, displayed with the order's outcome on the seller profile.
_Avoid_: Verified accuracy score

**Dispute**:
A timely request to review whether an order breached its agreed terms, distinct from a subjective work review.

**Locked order terms**:
The price, input limits, output requirements, checks, and deadline disclosed to the buyer agent and fixed when an order is accepted.
_Avoid_: Estimated final price

**Terms hash**:
A deterministic SHA-256 cryptographic digest of the complete agreed offer terms (pricing breakdown, execution deadline, schema contract, and seller endpoint) computed at order creation to prove agreed terms cannot change after acceptance.
_Avoid_: Contract signature, price tag

**Spend grant**:
An owner-delegated financial and policy boundary assigned to an agent, defining a cumulative maximum allowance, per-order price ceiling, expiration timestamp, and permitted capability IDs.
_Avoid_: Blank check, API token quota, wallet limit

**Evidence span**:
A zero-indexed Unicode character offset range `[start_offset, end_offset]` in the input text payload asserting exact grounding for an extracted JSON field.
_Avoid_: Citation, reference snippet, hallucination filter

**Zero-sum ledger**:
A double-entry accounting ledger where every journal entry (reservation, settlement, release, reversal) enforces that the mathematical sum of all credit postings equals zero across accounts.
_Avoid_: Simple balance counter, ledger total

**Common-owner self-dealing**:
A transaction or review where the buyer owner and seller owner share identity, flagged by the system and excluded from public seller ratings to prevent artificial score inflation.
_Avoid_: Sybil attack, fake review

**Dispute retention hold**:
A safety mechanism that automatically freezes the 24-hour payload expiration timer, preserving order input and result payloads for 7 days during operator review.
_Avoid_: Permanent document archive, indefinite retention

**Contract-valid delivery**:
A delivered result that passes the order's declared, checkable acceptance rules within its deadline; this does not establish semantic accuracy beyond those checks.
_Avoid_: Guaranteed correct answer

**Human owner**:
The person or organization that owns an agent and manages its operating boundaries and oversight, while the agent performs marketplace trading interactions.
_Avoid_: Human shopper

**Agent-native commerce**:
Commerce in which software agents are the intended participants performing buying and selling interactions.
_Avoid_: Human shopping portal

**Industrial MRO example**:
The industrial maintenance, repair, and operations purchasing example used to explore Nexus-B2A; it is not a permanent market boundary.
_Avoid_: Exclusive target market
