# VerFi Real-Artifact Intake Mirror Handoff

Goal: `GOV-VERFI-REAL-ARTIFACT-INTAKE-001`
Parent: `docs/governance/VERFI_EXTERNAL_EVIDENCE_MIRROR_HANDOFF.md`
Status: `IMPLEMENTED_PENDING_HOSTED_VALIDATION`

Installed surfaces:
- `docs/examples/interop/verfi_real_artifact_intake_contract.json`
- `docs/examples/VERFI_REAL_ARTIFACT_TEST_PROTOCOL.md`
- `scripts/validate_verfi_real_artifact_intake.py`
- `.github/workflows/validate_docs.yml`

Purpose: remove implementation-preparation ambiguity before a real VerFi artifact arrives. The lane now defines immutable artifact identity, accepted artifact classes, mandatory observables, deterministic negative/fail-closed outcomes, and the exact ten-test protocol to execute against a real artifact.

The repository explicitly preserves `artifact_instance_present=false`. No production VerFi record, evidence package, API output, schema, or Execution Verified Token specimen is claimed to exist.

Mandatory intake identity:
- artifact type
- source/transfer reference
- SHA-256 digest
- byte length
- observation time
- producer-asserted provenance posture

Mandatory implementation tests:
1. ARTIFACT_IDENTITY_BINDING
2. DIGEST_REPRODUCIBILITY
3. DISCLOSURE_VERSION_CONTINUITY
4. CHECKPOINT_CORRECTION_PRESERVATION
5. AUTHORIZATION_ENABLEMENT_CAUSALITY
6. COMPREHENSION_MISSING_NEGATIVE
7. TAMPER_FAIL_CLOSED
8. TEMPORAL_ORDER_VALIDATION
9. INDEPENDENT_RECONSTRUCTION
10. EXTERNAL_TOKEN_NO_AUTHORITY

Authority invariants remain false for provider execution authority, external-token execution/admissibility authority, Governance-minted Continuity receipt, inferred legal admissibility, and cognitive-state proof.

Implementation commits:
- intake contract: `b78fd43532e60365f5bafdb22386b70ba3c424af`
- test protocol: `0fbda00c801617bd72e5c2a769f4a8a7412a9026`
- validator: `e1dc3017229ca6b4e995247694b62cc36d90ee24`
- workflow integration: `d882cd3b289d95acfa2edd1cb3cbe90bc6b61e22`

Next gate: hosted validation of this exact tree, then bind run/job/head/merge evidence here and into Governance issue #21. After that, only receipt of a real VerFi artifact can advance implementation-level interoperability.
