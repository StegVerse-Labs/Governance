# External Evidence Provider Interface

## Purpose

This contract defines how telemetry, attestation, verification, audit, or bounded human-transition evidence systems may provide evidence to StegVerse without acquiring execution authority.

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

A provider-specific test profile may constrain or extend the evidence semantics without changing the generic envelope authority boundary. Such a profile remains evidence-only unless a separate, current Governance/StegCore authorization path admits the resulting commitment candidate.

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

Cryptographic validity proves integrity and signer association only. It does not prove current authority, consent, legitimacy, custody, comprehension, or admissibility.

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
- telemetry or transition-evidence capture interval and subject binding;
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

## VerFi human-transition evidence test profile

`docs/examples/interop/verfi_transition_cases.json` registers a bounded test profile for the external VerFi formalism candidate maintained in `Admissible-Existence/.github`.

The profile tests the publicly represented sequence:

```text
IDENTITY -> DISCLOSURE -> COMPREHENSION -> AUTHORIZATION -> SIGNATURE -> EVIDENCE
```

against StegVerse Governance without treating the external sequence as canonical StegVerse mathematics or as a source of execution authority.

Ten deterministic governance-lane cases are required:

```text
CLEAN_SEQUENCE
COMPREHENSION_MISSING
DISCLOSURE_DRIFT
AUTHORIZATION_LAPSED
EVIDENCE_TAMPER
TEMPORAL_DISORDER
AMBIGUOUS_COMPREHENSION
OVER_COLLECTION
INDEPENDENT_RECONSTRUCTION
HUMAN_MACHINE_SYMMETRY
```

The mandatory negative invariant is that a recorded signature cannot substitute for missing or ambiguous comprehension evidence. `COMPREHENSION_MISSING` must remain a non-ALLOW outcome even when both disclosure and signature are present.

`HUMAN_MACHINE_SYMMETRY` is comparison-only. It tests whether human and machine sequences can share transition vocabulary while preserving different evidence semantics; it cannot grant machine or human execution authority.

Until an actual VerFi evidence envelope, schema, or API output is supplied and independently reconstructed, this profile remains `TEST_CANDIDATE` rather than production interoperability proof.
