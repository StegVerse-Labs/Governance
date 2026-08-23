# VerFi Semantic Translation Mirror Handoff

Goal: `GOV-VERFI-SEMANTIC-TRANSLATION-001`
Parent: `docs/governance/VERFI_EXTERNAL_EVIDENCE_MIRROR_HANDOFF.md`
Status: `IMPLEMENTED_PENDING_HOSTED_VALIDATION`

Installed:
- `docs/examples/interop/verfi_semantic_translation.json`
- `scripts/validate_external_evidence_interop.py`

Purpose: make explicit that Admissible-Existence candidate classes and Governance terminal decisions are not identity-equivalent.

Validated mappings include:
- `ALLOW_CANDIDATE -> ALLOW` only after Governance evaluation.
- `AUTHORIZATION_INADMISSIBLE -> DENY`.
- disclosure-drift `REVIEW -> FAIL-CLOSED`.
- ambiguous-comprehension `REVIEW -> DENY`.
- `REVIEW_MINIMIZATION -> DENY`.
- `STRUCTURAL_COMPARISON_ONLY -> DENY / comparison.no_execution_authority`.

Required invariants:
- candidate classification never grants execution authority;
- Governance may resolve a candidate-layer review to DENY or FAIL-CLOSED;
- ALLOW_CANDIDATE is not ALLOW until Governance evaluates it;
- comparison-only can never authorize execution.

Commits:
- translation artifact: `0004b9416a61e1d8ff44a1cad970cb656e50de38`
- validator integration: `417567d31d5721c390c1285182a4640aa1ace97a`

Next gate: run the existing `Validate Governance Docs` path against this exact tree, bind run/job/head evidence, then update the parent VerFi handoff and issue #21. No VerFi product, legal, cognitive-state, Continuity, or execution authority is created by this lane.
