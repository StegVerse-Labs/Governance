# StegCore Release Policy Mirror Handoff

## Scope

- Repository: `StegVerse-Labs/Governance`
- Subject repository: `StegVerse-Labs/StegCore`
- Workflow: `.github/workflows/evaluate-stegcore-release.yml`
- Policy: `policies/stegcore-release-policy-v1.json`
- Decision artifact: `evidence/stegcore-release-decision.json`
- Authority effect: `NONE`

This handoff records the bounded repair of Governance's independent StegCore release-policy evaluator. It does not supersede `GOVERNANCE_MIRROR_HANDOFF.md`; that root handoff remains repository authority.

## Observed failure

Workflow run `32452877938` on Governance main commit `aec49c63be87a193f0e4bf52b87240f918609315` failed before policy evaluation. The `Acquire StegCore candidate and evidence` step attempted anonymous `raw.githubusercontent.com` reads and received HTTP 404 before any decision artifact was produced.

Connected repository inspection confirms at least `StegVerse-Labs/StegCore/evidence/release-candidate-request.json` exists on StegCore main. Therefore the failure is an acquisition-boundary failure, not evidence that the candidate file is absent and not a release-policy denial.

## Repair installed and verified

Commit `5fd6737a66245c9f9d03bc0b198c50bdb86f6abb` updates `.github/workflows/evaluate-stegcore-release.yml` so the acquisition path:

1. adds no new credential, token, or cross-repository authority;
2. records every required path that is inaccessible at the configured anonymous boundary;
3. emits a durable `FAIL-CLOSED` governance decision when required evidence cannot be acquired;
4. preserves `release_created=false`, `tag_created=false`, `deployment_authorized=false`, and `continuity_receipt_minted=false`;
5. permits normal independent policy evaluation only when the complete required evidence set is actually readable.

Hosted run `32454014552` proved the repair. Acquisition completed successfully as an observation step, normal policy evaluation was skipped because the evidence set was inaccessible, the fail-closed artifact was created, decision output resolved, artifact-boundary validation passed, the changed decision persisted, and release-policy issue reconciliation passed. The run remained red only because the final policy gate intentionally fails whenever the decision is not `ALLOW`.

The persisted decision is `FAIL-CLOSED`, decision hash `7d41889bfdbdf11f40669d9e7316e512ba01c89a0de59ea3969f6072b222e324`. It records all six required StegCore inputs as inaccessible at the anonymous raw boundary, `credential_escalation_attempted=false`, and no release/tag/deployment/continuity authority.

An inaccessible projection is not treated as a failed StegCore runtime gate and is not converted into release authority.

## Current state

```text
repair_implemented: true
hosted_repair_validation: verified
workflow_run: 32454014552
release_decision: FAIL-CLOSED
release_created: false
tag_created: false
deployment_authorized: false
continuity_receipt_minted: false
credential_escalation_authorized: false
```

## Exact next actions

1. Keep the release goal open while the acquisition boundary remains fail-closed.
2. Restore evidence availability only through a TV/TVC-governed projection or another explicitly authorized repository-readable transfer; do not add a GitHub-token runtime authority merely to make the evaluator pass.
3. Re-run the actual independent release gates only after all required evidence is readable and commit/hash bindings can be verified.
4. An `ALLOW` decision, if eventually produced, permits only the separately governed annotated-tag action declared by policy. It is not itself a tag, release, deployment, runtime proof, continuity receipt, or activation.
5. Propagate release evidence to Site, Publisher, admissibility-wiki, and stegguardian-wiki only if and when the exact release contract reaches the required released state.

## Remaining required evidence inputs

The evaluator requires these StegCore inputs:

- `evidence/release-candidate-request.json`
- `evidence/runtime-validation.json`
- `evidence/release-readiness.json`
- `evidence/downstream-verification-results.json`
- `evidence/governance-freshness.json`
- `pyproject.toml`

No placeholder or synthesized evidence may satisfy these requirements.
