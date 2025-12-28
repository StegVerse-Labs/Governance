# Governance Decision Record (GDR)

A Governance Decision Record (GDR) is the **output** of governance evaluation.
It is **auditable**, **portable**, and **downstream-consumable**.

Governance runs ONLY on verified inputs (e.g., verified Continuity Receipts).
Governance does NOT perform cryptographic verification.

---

## Contract

A GDR MUST include:

- `gdr_version` (currently `1.0`)
- `decision_id`
- `decision` (`allow | deny | require_review | recommend`)
- `policy.policy_id`
- `policy.policy_version`
- `evaluated_inputs.source`
- `evaluated_inputs.receipt_ids`
- `issued_at` (epoch seconds)
- `rationale` (human-readable)

Optional fields:

- `evaluated_inputs.bundle_hash`
- `notes` (string list)
- `hints` (machine hints)
- `trace` (correlation / trace metadata)

---

## Example

```json
{
  "gdr_version": "1.0",
  "decision_id": "gdr_2025_12_24_001",
  "decision": "allow",
  "policy": {
    "policy_id": "policy.accept_valid_receipt_chain",
    "policy_version": "1.0"
  },
  "evaluated_inputs": {
    "source": "stegid.continuity_receipts",
    "receipt_ids": ["r0"],
    "bundle_hash": null
  },
  "issued_at": 1766530000,
  "rationale": "Receipt chain verified; signing key is known and not revoked.",
  "notes": ["No anomalies detected."]
}
```

---

## Design Guarantees

- Deterministic for given inputs + policy version
- Does not modify receipts
- Does not claim authority over truth
- Safe for humans + AI consumers

## Decision Stability

A GDR reflects a decision **at the time of issuance**.

New information MAY:
- produce a new GDR
- recommend review
- downgrade confidence via TRACE

New information MUST NOT:
- silently invalidate prior GDRs
- rewrite historical decisions
- alter issued records

Supersession requires a new GDR referencing the prior decision_id.
