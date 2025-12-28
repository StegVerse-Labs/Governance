# GDR Enforcement Profile (Governance-First Automation Boundary)

## Purpose

This document defines the **minimum rules** downstream systems MUST follow when using
a **Governance Decision Record (GDR)** to gate actions.

Governance is authoritative over **decisions**, not **truth**.
Downstream systems MUST treat the GDR as the **automation boundary**.

---

## Definitions

### GDR (Governance Decision Record)
A deterministic, auditable output produced by Governance from bounded inputs.
See: `docs/governance/GOVERNANCE_DECISION_RECORD.md`

### Irreversible Action
Any action that:
- changes external state (money, secrets, identity, network egress, public publish),
- creates or modifies authority (permissions, tokens, keys, policy versions),
- makes data or artifacts harder to retract (publication, distribution, anchoring),
- could harm users if performed incorrectly.

If unsure: **treat as irreversible**.

---

## Enforcement Rule (Hard Requirement)

**No downstream system may execute an irreversible action without a valid GDR.**

Valid means:
1. The GDR matches the schema (`schemas/gdr.schema.json`)
2. The policy referenced is known to the system (policy_id + policy_version)
3. The evaluated inputs are bounded and acceptable (see below)
4. The decision permits the action under the system’s local mapping

If any check fails → **deny-by-default**.

---

## Minimum Required GDR Fields for Enforcement

Downstream systems MUST require these fields to exist and be non-empty:

- `gdr_version`
- `decision_id`
- `decision`
- `policy.policy_id`
- `policy.policy_version`
- `evaluated_inputs.source`
- `evaluated_inputs.receipt_ids` (must be present even if empty is disallowed by local policy)
- `issued_at`
- `rationale`

Recommended (strongly):
- `trace` with at least one correlation key, e.g. `trace.correlation_id` or `trace.request_id`

---

## Bounded Inputs (What Governance May Evaluate)

Downstream systems MUST reject any GDR whose rationale or metadata indicates that Governance
evaluated unbounded inputs.

Governance may evaluate ONLY:
- **Verified Continuity Receipts** (from StegID)
- **TRACE Signal Bundles** (from StegTrace) — bounded, confidence-scored, non-authoritative
- **Versioned policy configuration**
- **Explicit execution context** (optional)

Governance MUST NOT evaluate raw documents, screenshots, testimony, rumors, or unverified claims.

See: `docs/governance/TRACE_SIGNAL_BUNDLE.md`

---

## Decision → Action Mapping (Default)

Downstream systems MUST implement a strict mapping:

- `allow` → action may proceed (subject to local constraints)
- `deny` → action MUST NOT proceed
- `require_review` → action MUST NOT proceed without a human approval step
- `recommend` → non-irreversible action may proceed; irreversible actions MUST still require `allow`

**Default policy:** if the system doesn’t recognize the decision value, treat as `deny`.

---

## Non-Retroactivity

A GDR is immutable and non-retroactive:
- New information produces a **new GDR**
- Downstream systems MUST NOT mutate old GDRs to “update history”

(Downstream may store supersession links, but must preserve originals.)

---

## Required Local Hardening (Downstream)

Every enforcing system (StegOps, StegTalk, StegTV, StegTrace publish, etc.) MUST:
- Deny-by-default on missing/invalid GDR
- Log an auditable “why denied” event (no secrets)
- Bind irreversible actions to a specific `decision_id`
- Record the input `receipt_ids` used for gating

---

## Notes

This profile is deliberately minimal. It defines the **boundary** that prevents
future headaches (silent execution, policy drift, unbounded inputs, and unclear audit trails).
