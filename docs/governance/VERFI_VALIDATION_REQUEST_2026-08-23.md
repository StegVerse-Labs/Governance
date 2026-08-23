# VerFi Governance Exact-Tree Validation Request — 2026-08-23

Goal: `GOV-VERFI-EXTERNAL-EVIDENCE-001`

Source of truth: `docs/governance/VERFI_EXTERNAL_EVIDENCE_MIRROR_HANDOFF.md`.

This request forces a pull-request execution of the existing `Validate Governance Docs` lane against a tree based on current `main` after the VerFi transition-prerequisite hardening.

Required observations:

- the five existing generic external-evidence envelopes still validate;
- all ten VerFi canonical governance cases validate;
- the derived missing-disclosure and missing-signature regressions remain non-ALLOW;
- `signature_cannot_substitute_for_comprehension=true` remains enforced;
- `external_provider_execution_authority=false` and `continuity_receipt_minted=false` remain enforced.

A successful PR run establishes hosted validation of the proposed tree only. It does not by itself satisfy the stricter exact-current-`main` commit gate; merge/current-main evidence must remain separately bound before that gate is released.
