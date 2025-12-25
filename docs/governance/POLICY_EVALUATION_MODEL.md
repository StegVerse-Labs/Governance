# Policy Evaluation Model

## Overview

Policy evaluation operates exclusively on **verified inputs**.
Unverified data MUST NOT enter the policy engine.

Inputs are immutable.
Outputs are auditable.

---

## Inputs

Policies may evaluate:

- Verified Continuity Receipts
- Receipt metadata (timestamps, sequence, key IDs)
- Policy configuration data
- Explicit context (environment, request type)

All cryptographic verification MUST be completed prior to evaluation.

---

## Outputs

A policy evaluation MUST emit a **Governance Decision Record (GDR)** containing:

- decision (`allow | deny | require_review | recommend`)
- policy_id
- policy_version
- evaluated_receipts (IDs)
- timestamp
- rationale (human-readable)
- notes (optional machine hints)

Governance output is **advisory or gating**, never cryptographic.

---

## Determinism

Given the same:
- receipts
- policy version
- configuration

The policy engine MUST produce the same result.

This guarantees:
- reproducibility
- auditability
- AI alignment safety

---

## Failure Modes

Policy evaluation may fail due to:

- Missing required receipt inputs
- Unsupported policy version
- Invalid configuration

Failures MUST be explicit and non-silent.

---

## Non-Goals

Policy evaluation does NOT:
- Perform identity verification
- Validate cryptographic signatures
- Modify receipts
- Create authority outside policy scope
