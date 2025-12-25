# Resolver Contract

## Purpose

The resolver is the minimal governance engine component that transforms:

**Verified Inputs → Governance Decision Record (GDR)**

---

## Inputs (required)

- Verified receipt(s) from StegID
- Policy configuration (`policy_id` + `policy_version`)
- Optional execution context (trace info, request metadata)

---

## Output (required)

- A valid GDR

---

## Strict Rules

The resolver MUST NOT:

- Call StegID verification internally
- Mutate receipts
- Invent identity
- Output decisions without referencing evaluated inputs

---

## Principle

> The resolver decides policy outcomes, not truth.
