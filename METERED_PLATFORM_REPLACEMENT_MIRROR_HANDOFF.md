# Metered Platform Replacement Mirror Handoff

## Source of Truth

This file is the current continuation record for the Metered Platform Replacement and Sovereign Infrastructure workstream in `StegVerse-Labs/Governance`.

Read `GOVERNANCE_MIRROR_HANDOFF.md` first for repository-wide authority and active integration boundaries. This workstream is additive and does not supersede the broader Governance handoff.

## Current Goal

Identify external financial drains, preserve privacy-safe cost evidence, rank replacement candidates deterministically, govern migration design, and deny provider retirement until every continuity, custody, rollback, and successor-health gate is verified.

## Current Branch and Review Surface

```text
Repository: StegVerse-Labs/Governance
Branch: agent/metered-platform-replacement
Draft PR: #3
StegCore runtime issue: StegVerse-Labs/StegCore#26
Manual user action required: false
```

## Implemented Files

```text
docs/governance/METERED_PLATFORM_REPLACEMENT.md
data/external_dependency_registry.json
data/external_cost_evidence.json
scripts/validate_external_dependency_registry.py
scripts/validate_external_cost_evidence.py
scripts/score_external_dependencies.py
scripts/validate_metered_replacement_gdrs.py
scripts/build_metered_replacement_status.py
scripts/sync_metered_replacement_runtime_issue.py
docs/examples/fixtures/metered_replacement_selection_gdr.json
docs/examples/fixtures/metered_replacement_retirement_denied_gdr.json
.github/workflows/validate_external_dependency_registry.yml
.github/workflows/metered_replacement_continuation.yml
```

The leading dot in workflow paths is retained here because this is a machine continuation record.

## Registered External Dependencies

```text
Render
PyPI and related package services
GitHub
Cloud storage and compute providers
GoDaddy
Unknown recurring services
```

Costs remain unknown until privacy-safe evidence records are supplied and verified. Unknown cost does not mean zero cost.

## Governance Decisions

1. Registry presence does not authorize cancellation.
2. Replacement selection authorizes only inventory, dependency mapping, successor design, and parallel-operation preparation.
3. Replacement design does not authorize traffic cutover, credential revocation, deletion, account closure, or retirement.
4. Retirement requires a separate Governance Decision Record.
5. Retirement fails closed if any required evidence is missing.
6. Cost evidence stored in the repository must be normalized and privacy-safe; raw statements, account numbers, credentials, and personal financial records are prohibited.
7. Governance and StegCore do not mint continuity receipts through this workstream.

## Canonical Runtime Cases

```text
replacement selection:
  ALLOW / replacement.selection_allowed
  scope: REPLACEMENT_DESIGN_ONLY
  provider_retirement_authority: false
  cancellation_authority: false
  continuity_receipt_minted: false

retirement with incomplete evidence:
  DENY / retirement.evidence_incomplete
  scope: PROVIDER_RETIREMENT
  provider_retirement_authority: false
  cancellation_authority: false
  continuity_receipt_minted: false
```

## Required Retirement Evidence

```text
asset_inventory_complete
export_verified
successor_health_verified
parallel_operation_passed
rollback_verified
secrets_rotated
traffic_cutover_verified
master_records_custody_recorded
```

## Machine-Owned Continuation

`.github/workflows/metered_replacement_continuation.yml` owns repository-side continuation after merge.

It automatically:

```text
validate registry, cost evidence, and canonical GDR fixtures
-> build deterministic fail-closed status
-> replay status generation and compare exact output
-> synchronize the StegCore runtime issue when cross-repository credentials are available
-> retain changed status on main
-> repeat daily and on governed-input changes
```

The workflow does not infer missing financial facts, fabricate cost evidence, authorize cancellation, or perform provider retirement. Absence of a cross-repository token is recorded as a non-mutating fail-closed condition rather than converted into a manual user task.

Generated state:

```text
reports/metered-platform-replacement-status.json
```

Every dependency record declares `manual_action_required: false`. Missing evidence remains a machine-readable blocker.

## Validation State

The policy, registry, cost-evidence, scoring, documentation, ingestion integration, and original canonical GDR extension reached a fully green PR head before the machine-owned continuation extension.

The current head must pass:

```text
Validate Governance (schema + docs)
Validate Governance Docs
Validate External Dependency Registry
Metered Replacement Continuation
Test Readiness
Forward PR to StegVerse AI Bridge
```

Do not mark the workstream integration-ready until all current-head checks pass.

## Cross-Repository Ownership

```text
StegVerse-Labs/Governance
  policy
  dependency registry
  cost-evidence boundary
  deterministic priority rules
  canonical GDR fixtures
  repository validators
  machine-owned status and task synchronization

StegVerse-Labs/StegCore
  deterministic runtime evaluation
  runtime receipts
  mutation tests
  replay verification
  commit-bound runtime evidence

master-records
  verified cost-evidence custody
  migration-evidence custody
  retirement-evidence custody

provider adapter or infrastructure repositories
  inventory collection
  export
  successor implementation
  parallel operation
  rollback
  traffic cutover
  provider-specific retirement execution
```

StegCore issue #26 is sequenced after or independently from the active commit-coherence PR #18 and must not disrupt that branch.

## Remaining Work

```text
StegVerse-Labs/Governance
  -> observe all current-head PR #3 checks automatically
  -> repair only exact failures without weakening authority boundaries
  -> merge only after repository policy permits and checks pass

StegVerse-Labs/StegCore
  -> implement issue #26 after current handoff sequencing permits
  -> evaluate both canonical fixtures
  -> publish commit-bound passing runtime evidence

Financial discovery
  -> ingest normalized privacy-safe evidence when available
  -> identify additional merchants from verified evidence
  -> calculate verified monthly and annual drain automatically

Provider migration
  -> select first target only from verified evidence and deterministic score
  -> generate provider-specific asset inventory through its owning adapter
  -> implement successor and parallel-operation plan
  -> retain rollback until migration and custody are verified
```

No repository-side continuation step requires a person to dispatch a workflow, copy status, update the StegCore task, generate a report, or transcribe blockers.

## Release and Propagation Posture

No tag, release, cancellation, account closure, deletion, DNS transfer, credential revocation, production traffic cutover, or provider retirement is authorized.

After Governance and StegCore runtime evidence are complete, verify pertinent propagation to:

```text
StegVerse-Labs/Site
GCAT-BCAT-Engine/Publisher
StegVerse-Labs/admissibility-wiki
StegVerse-002/stegguardian-wiki
```

## Completion Assessment

```text
Policy and authority boundary: implemented
Dependency registry: implemented
Privacy-safe cost-evidence contract: implemented
Deterministic priority scoring: implemented
Canonical selection and retirement-denial fixtures: implemented
Repository validation: implemented
Machine-owned status generation: implemented
Automatic StegCore task synchronization: implemented, credential-dependent and fail-closed
StegCore runtime evaluator: task created, not yet built
Verified financial costs: not yet recorded
Provider inventories: not yet built
Provider replacement runtimes: not yet built
Migration evidence custody: not yet built
Provider retirements: none authorized or completed
Manual repository continuation dependency: none
```

## Archive Status

This handoff, Governance PR #3, StegCore issue #26, canonical fixtures, validators, workflows, generated status path, workflow history, and repository commits preserve all workstream continuation state. No prior conversation context is required.
