# Resolver Contract

## Purpose

The resolver is the minimal governance engine component that transforms:

**Verified Inputs → Governance Decision Record (GDR)**

---

## Inputs (required)

- Verified receipt(s) from StegID
- Policy configuration (policy_id + policy_version)
- Optional execution context (trace info, request metadata)

---

## Output (required)

- A valid GDR (see `docs/GOVERNANCE_DECISION_RECORD.md`)

---

## Strict Rules

The resolver MUST NOT:

- call StegID verification internally
- mutate receipts
- invent identity
- output decisions without referencing evaluated inputs

---

## Principle

> The resolver decides policy outcomes, not truth.
