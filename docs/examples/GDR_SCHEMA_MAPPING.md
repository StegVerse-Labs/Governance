# GDR Schema Mapping Notes

## Purpose

This note maps Governance Decision Record examples to the current GDR shape without requiring prior chat context. It also defines the examples-only extension for judgment conditions, signal admission and state formation, and execution-boundary admissibility.

## Example fixtures

Base examples:

- `docs/examples/fixtures/dual_quorum_gdr.json`
- `docs/examples/fixtures/drift_review_gdr.json`

Three-layer negative examples:

- `docs/examples/fixtures/condition_degraded_judgment_gdr.json`
- `docs/examples/fixtures/signal_admission_drift_gdr.json`
- `docs/examples/fixtures/governance_validation_of_drift_gdr.json`

## Base field mapping

| Example field | Meaning | Target schema consideration |
| --- | --- | --- |
| `gdr_version` | Version of the record shape | Remains `1.0` until a canonical schema revision is approved. |
| `decision_id` | Stable decision record identifier | Maps to the GDR identifier. |
| `decision` | Governance result | Bounded to `allow`, `deny`, `require_review`, or `recommend`. |
| `policy` | Policy identity and version | Must identify both `policy_id` and `policy_version`. |
| `evaluated_inputs` | Structured evidence summary | Must preserve source and receipt references. |
| `issued_at` | Machine-readable issuance time | Integer epoch value in examples. |
| `rationale` | Human-readable explanation | Explains the result but does not expand authority. |
| `hints` | Constraints or workflow guidance | Advisory unless a runtime schema explicitly binds it. |
| `trace` | Example provenance | Non-authoritative diagnostic metadata. |

## Three-layer extension

The extension is additive. It does not change the allowed top-level GDR decision vocabulary and does not grant execution authority.

### `judgment_conditions`

| Field | Requirement | Purpose |
| --- | --- | --- |
| `workload_state` | required string | Declares whether workload conditions supported meaningful judgment. |
| `time_pressure` | required string | Declares material timing pressure. |
| `isolation_state` | required string | Declares access to review, assistance, or contest. |
| `refusal_available` | required boolean | Records whether refusal was practically available. |
| `operator_recoverability` | required string | Records whether operator authority could be recovered after degradation or interruption. |
| `condition_receipt_ids` | required array | References evidence for the condition declaration. |

The section records decision conditions, not a biometric or psychological score. A future implementation must not infer medical, employment, or legal fitness from these example values.

### `signal_admission`

| Field | Requirement | Purpose |
| --- | --- | --- |
| `admitted_signal_refs` | required array | Identifies signals used to construct state. |
| `excluded_signal_refs` | required array | Identifies known excluded signals. |
| `transformations` | required array | Preserves filtering, ranking, compression, or other transformations. |
| `missing_inputs` | required array | Declares inputs known to be absent. |
| `uncertainty_state` | required string | Declares unresolved uncertainty. |
| `reference_state_hash` | required string | Identifies the state actually evaluated. |
| `authorized_reference_state_hash` | conditional string | Identifies the authorized comparison state when continuity is evaluated. |
| `reconstruction_available` | required boolean | States whether another evaluator can reconstruct the state basis. |

When `reference_state_hash` differs from `authorized_reference_state_hash`, the resolver must not treat otherwise-valid policy or authority checks as sufficient.

### `execution_boundary`

| Field | Requirement | Purpose |
| --- | --- | --- |
| `actor_authority_ref` | required string | References current actor authority. |
| `policy_ref` | required string | References the policy applied at commit time. |
| `delegation_ref` | required string | References current delegation. |
| `evidence_refs` | required array | References evidence used for the execution result. |
| `affected_entity_refs` | required array | Identifies affected entities represented in evaluation. |
| `recoverability_profile` | required string | Declares whether consequences can be recovered. |
| `validity_window` | required string | Bounds the period in which the result is valid. |
| `result` | required enum | Bounded to `ALLOW`, `DENY`, or `FAIL-CLOSED`. |
| `receipt_ref` | required string | References the execution-boundary receipt. |

The uppercase execution result is distinct from the lowercase governance recommendation. A GDR can explain governance reasoning while the execution boundary independently fails closed.

## Required invariants

1. The three sections must be separately inspectable.
2. Human approval cannot repair missing or unreconstructable state evidence.
3. Valid policy and authority checks cannot override failed reference-state continuity.
4. `reconstruction_available=false` cannot produce `ALLOW`.
5. `refusal_available=false` with materially degraded recoverability cannot produce `ALLOW` without a separately documented emergency authority path.
6. A failed reference-state continuity check must produce `DENY` or `FAIL-CLOSED`.
7. Example records must never expand execution authority.

## Automated enforcement

`scripts/validate_gdr_examples.py` validates:

- the base GDR shape for every JSON fixture;
- presence of all three required negative fixtures;
- required fields for all three architecture layers;
- fixture-specific denial and fail-closed invariants;
- separation of valid authority/policy checks from failed state continuity.

The `Validate Governance Docs` workflow runs this validator automatically on relevant pushes and pull requests. Manual workflow dispatch remains available only as a recovery mechanism, not as the primary validation path.

## Runtime placement

The documentation and examples remain owned by `StegVerse-Labs/Governance`. Runtime resolver enforcement should be implemented in a code-bearing boundary repository after placement analysis. Current candidates are StegCore and SCW; Governance should remain the canonical policy and fixture source unless a later handoff records a different assignment.

## Rule

Examples demonstrate governance reasoning, evidence boundaries, and expected resolver behavior. They do not authorize actions, infer human fitness, or replace canonical policy, delegation, or evidence artifacts.
