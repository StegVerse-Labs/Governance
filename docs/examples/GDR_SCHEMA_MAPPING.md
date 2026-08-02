# GDR Schema Mapping Notes

## Purpose

This note maps Governance Decision Record examples to the current GDR shape without requiring prior chat context. It also defines the examples-only extension for judgment conditions, signal admission and state formation, execution-boundary admissibility, and relationship/outcome commitments.

## Example fixtures

Base examples:

- `docs/examples/fixtures/dual_quorum_gdr.json`
- `docs/examples/fixtures/drift_review_gdr.json`

Three-layer negative examples:

- `docs/examples/fixtures/condition_degraded_judgment_gdr.json`
- `docs/examples/fixtures/signal_admission_drift_gdr.json`
- `docs/examples/fixtures/governance_validation_of_drift_gdr.json`

Relationship/outcome examples:

- `docs/examples/relationship-outcome/constructive_participation_allow.json`
- `docs/examples/relationship-outcome/attention_success_outcome_failure.json`

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

Records workload, pressure, isolation, practical refusal, operator recoverability, and condition evidence without inferring medical, employment, or legal fitness.

### `signal_admission`

Records admitted and excluded signals, transformations, missing inputs, uncertainty, reference-state hashes, and reconstruction availability. Human approval cannot repair missing or unreconstructable state evidence.

### `execution_boundary`

Records actor authority, policy, delegation, evidence, affected entities, recoverability, validity, result, and receipt. The uppercase execution result is distinct from the lowercase governance recommendation and remains bounded to `ALLOW`, `DENY`, or `FAIL-CLOSED`.

## Relationship and outcome commitment mapping

The relationship commitment contract is an evidence input to governance reasoning. It does not replace policy, delegation, consent, identity, execution-boundary checks, or admissibility.

| Relationship field | GDR mapping | Rule |
| --- | --- | --- |
| `commitment_id` | `evaluated_inputs.relationship_commitment_ref` | Stable reference to the evaluated commitment. |
| `declared_goal` | `evaluated_inputs.relationship_goal` | Defines the outcome against which direction is measured. |
| `target_participants` | `evaluated_inputs.affected_entity_refs` | Identifies intended participants; it grants no authority. |
| `framing_posture` | `evaluated_inputs.relationship_posture` | Records constructive, adverse-evidence, neutral, or outcome-inverting posture. |
| `observation_signals` | `evaluated_inputs.evidence_refs` | Names observable signals required for later evaluation. |
| `attention_result` | `trace.relationship_attention_result` | Visibility evidence is diagnostic and cannot independently establish success. |
| `relationship_effect` | `trace.relationship_effect` | Records constructive, neutral, degrading, or unknown effect. |
| `outcome_direction` | `trace.relationship_outcome_direction` | Records movement toward, neutral to, or away from the declared goal. |
| `decision` | `hints.relationship_disposition` | Maps `ALLOW`, `ALLOW_WITH_OBSERVATION`, `REPAIR_REQUIRED`, or `DENY` into bounded governance guidance. |
| `continuation_owner` | `hints.continuation_owner` | Must name `organization/repository:path`; unnamed external continuation is invalid. |
| `completion_evidence` | `evaluated_inputs.completion_evidence_ref` | Names the receipt required to prove completion. |

### Relationship invariants

1. Attention success is not equivalent to constructive outcome success.
2. `attention_result=success` with `outcome_direction=away_from_goal` cannot produce relationship disposition `ALLOW`.
3. `relationship_effect=degrading` requires `REPAIR_REQUIRED` or `DENY`.
4. Constructive framing does not suppress adverse evidence; adverse evidence must remain inspectable.
5. The relationship commitment must preserve `grants_execution_authority=false` and `mints_continuity_receipt=false`.
6. A relationship disposition cannot override a failed judgment, signal-admission, policy, delegation, consent, identity, evidence, or execution-boundary check.

## Required invariants

1. The architecture layers must remain separately inspectable.
2. Human approval cannot repair missing or unreconstructable state evidence.
3. Valid policy and authority checks cannot override failed reference-state continuity.
4. `reconstruction_available=false` cannot produce `ALLOW`.
5. A failed reference-state continuity check must produce `DENY` or `FAIL-CLOSED`.
6. Relationship evidence cannot grant execution authority or mint Continuity receipts.
7. Example records must never expand execution authority.

## Automated enforcement

- `scripts/validate_gdr_examples.py` validates the base and three-layer GDR examples.
- `scripts/validate_relationship_outcomes.py` validates the relationship schema, canonical fixtures, outcome-inversion rules, continuation-owner location, non-authority, and non-minting boundaries.
- `scripts/validate_docs.py` requires the relationship architecture, handoff, schema, fixtures, validator, task registry, runner, and workflows.
- `Validate Governance Docs` runs all validators on relevant pushes and pull requests.

## Runtime placement

Documentation, contracts, examples, and validation remain owned by `StegVerse-Labs/Governance`. A future runtime consumer may evaluate the commitment only by reference and must preserve all authority boundaries. Governance does not claim deployment authority, legal adjudication, or Continuity receipt minting.

## Rule

Examples demonstrate governance reasoning, evidence boundaries, expected resolver behavior, and relationship/outcome classification. They do not authorize actions, infer human fitness, or replace canonical policy, delegation, consent, identity, or evidence artifacts.
