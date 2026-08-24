# VerFi Real-Artifact Test Protocol

Status: `READY_FOR_REAL_ARTIFACT_NO_ARTIFACT_BOUND`

This protocol defines the next interoperability gate for the bounded VerFi external-formalism candidate. It does not claim that a production VerFi artifact has been received or validated.

## Intake

A received artifact must first be bound by immutable identity using artifact type, source/transfer reference, SHA-256 digest, byte length, observation time, and producer-asserted provenance. The raw artifact is evidence input only; it cannot grant StegVerse execution, AE admissibility, Continuity receipt, legal, publication, or release authority.

Accepted first artifacts include a consent record, sealed evidence package, implementation schema, API output, or Execution Verified Token specimen.

## Required observations

Where present in the external representation, reconstruction attempts must preserve identity binding, exact disclosure version, comprehension checkpoint events, checkpoint correction history, authorization enablement, signature/commit event, integrity proof, and temporal ordering.

Absence of a required observable is itself a bounded result and must not be silently synthesized.

## Required test sequence

1. `ARTIFACT_IDENTITY_BINDING` — bind immutable identity before semantic interpretation.
2. `DIGEST_REPRODUCIBILITY` — independent digest calculation must reproduce the bound digest.
3. `DISCLOSURE_VERSION_CONTINUITY` — presented and authorized disclosure identity/version must remain continuous.
4. `CHECKPOINT_CORRECTION_PRESERVATION` — if a checkpoint is missed and re-presented, the original failure and correction must both remain reconstructable.
5. `AUTHORIZATION_ENABLEMENT_CAUSALITY` — authorization enablement must occur only after required checkpoint state is established; mere later correlation is insufficient.
6. `COMPREHENSION_MISSING_NEGATIVE` — disclosure plus signature without distinguishable comprehension evidence must remain non-ALLOW.
7. `TAMPER_FAIL_CLOSED` — integrity mutation must fail closed.
8. `TEMPORAL_ORDER_VALIDATION` — authorization/signature evidence preceding prerequisite evidence must fail closed.
9. `INDEPENDENT_RECONSTRUCTION` — an independent verifier must reconstruct the same bounded transition sequence and result from the immutable package.
10. `EXTERNAL_TOKEN_NO_AUTHORITY` — any VerFi-named Execution Verified Token may be evidence, but cannot become StegVerse/AE execution or admissibility authority.

## Result discipline

The test harness must preserve `ALLOW`, `DENY`, and `FAIL-CLOSED` as Governance outcomes and may preserve review posture upstream. An artifact cannot be promoted to production interoperability merely because it parses or because its publisher asserts validity.

## Activation criterion

This protocol becomes executable against VerFi implementation evidence only when an actual artifact is supplied and its immutable identity is bound. Until then, the protocol is complete preparation, not completed interoperability proof.
