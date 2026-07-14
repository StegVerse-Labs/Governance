# External Evidence Provider Interface

## Purpose

This contract defines how telemetry, attestation, verification, or audit systems may provide evidence to StegVerse without acquiring execution authority.

An external provider produces evidence. Governance determines whether that evidence is current, complete, authorized, continuous, and admissible for a commitment candidate. StegCore owns the runtime decision.

## Envelope

Every external evidence envelope uses `external_evidence_envelope_version: "1.0"` and contains:

- `envelope_id`
- `provider`
- `subject`
- `capture`
- `claims`
- `integrity`
- `authorization`
- `freshness`
- `evidence_refs`
- `prior_hash`
- `issued_at`

### Provider

`provider` identifies the evidence producer and its declared scope:

- `provider_id`
- `provider_type`: `telemetry`, `attestation`, `verification`, or `composite`
- `public_key_ref`
- `declared_scope`

### Subject and capture

`subject` binds evidence to the observed actor, target, workload, device, or run.

`capture` defines:

- `started_at`
- `ended_at`
- `execution_context`
- `reference_state_hash`

### Claims and integrity

`claims` is a list of typed assertions. Each claim contains `claim_id`, `claim_type`, `value`, and `evidence_digest`.

`integrity` contains:

- `content_digest`
- `signature_algorithm`
- `signature`
- `chain_valid`

Cryptographic validity proves integrity and signer association only. It does not prove current authority, consent, legitimacy, custody, or admissibility.

### Authorization and freshness

`authorization` contains:

- `provider_authorized`
- `authorization_ref`
- `scope_match`

`freshness` contains:

- `valid_from`
- `valid_until`
- `evaluated_at`
- `is_current`

## Commitment Candidate Mapping

A valid envelope maps into a StegVerse commitment candidate containing:

- actor, target, scope, action, and execution context;
- policy, delegation, consent, and identity references;
- evidence references and digests;
- telemetry capture interval and subject binding;
- prior-hash linkage;
- validity window;
- reference-state hash;
- recoverability profile;
- provider authorization posture.

The mapper never emits execution authority, custody, legal adjudication, insurance acceptance, regulatory recognition, or a Continuity receipt.

## Canonical Outcomes

| Case | Expected result | Reason |
|---|---|---|
| valid | ALLOW | `ok` |
| stale | DENY | `evidence.stale` |
| drifted | FAIL-CLOSED | `evidence.reference_state_drift` |
| incomplete | DENY | `evidence.incomplete` |
| unauthorized provider | DENY | `evidence.provider_unauthorized` |

All cases require `continuity_receipt_minted=false` and `evidence_provider_execution_authority=false`.
