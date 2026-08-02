# StegTrace Bootstrap Mirror Handoff

## Active goal

- Goal ID: `STEGTRACE-ENGINE-V0`
- Owner during repository absence: `StegVerse-Labs/Governance`
- Target repository: `StegVerse-Labs/StegTrace`
- Target branch after repository creation: `bootstrap/stegtrace-v0`
- Goal: install and validate the shared StegTrace engine bootstrap, then continue toward persistent evaluation, reevaluation, and application-profile integration.
- Related Governance architecture: Judgment-Signal-Execution Workstream

## Source of truth

Until `StegVerse-Labs/StegTrace/STEGTRACE_MIRROR_HANDOFF.md` exists on the target repository default branch, this file, the live workflow, its receipt, and the bootstrap issue are the authoritative continuation records.

Read before changing:

1. `GOVERNANCE_MIRROR_HANDOFF.md`
2. `docs/governance/TRACE_INTEGRATION.md`
3. `docs/governance/TRACE_SIGNAL_BUNDLE.md`
4. `schemas/trace_signal_bundle.schema.json`
5. this handoff
6. `scripts/bootstrap_stegtrace.py`
7. `.github/workflows/bootstrap-stegtrace.yml`
8. `evidence/stegtrace-bootstrap/latest.json`, when present

## Decisions preserved

- `StegTrace` is the shared evaluation engine.
- `StegTalk/trace`, `StegProv/trace`, and `StegFREEDOM/trace` are application-level profiles, not separate engines.
- TRACE outputs confidence and provenance assessments; it does not verify identity, establish truth, authorize execution, or replace Governance.
- New evidence creates new immutable evaluation records and explicit confidence deltas; prior evaluations are not overwritten.
- Research/publication repositories consume TRACE-processed outputs while preserving source and evaluation references.

## Completed work

- Governance-side TRACE integration and bounded consumer contract exist.
- A deterministic, idempotent bootstrap installer is committed on `feature/stegtrace-bootstrap-automation` at `scripts/bootstrap_stegtrace.py`.
- A scheduled and manually dispatchable observer/installer is committed at `.github/workflows/bootstrap-stegtrace.yml`.
- The installer contains the canonical initial StegTrace file set and creates or updates a target bootstrap branch and pull request.
- The workflow writes and uploads an inspectable state receipt.
- Governance issue #1 records the target repository creation boundary.

## Machine-owned task

### `STEGTRACE-ENGINE-V0-BOOTSTRAP`

- Owner repository: `StegVerse-Labs/Governance`
- Executor: `scripts/bootstrap_stegtrace.py`
- Trigger: hourly schedule or manual workflow dispatch
- Target: `StegVerse-Labs/StegTrace`
- Deduplication: workflow concurrency group plus fixed target branch and open-PR lookup
- States: `COMPLETE`, `BLOCKED`, `RETRY`, `REVIEW_REQUIRED`, `FAILED`
- Persistent receipt: `evidence/stegtrace-bootstrap/latest.json`
- Workflow artifact: `stegtrace-bootstrap-receipt`
- Release condition: GitHub API observation of `StegVerse-Labs/StegTrace` succeeds

## Human-authority boundary

Creating a new GitHub repository is not exposed by the connected repository mutation tools. The precise boundary is creation of public repository `StegVerse-Labs/StegTrace` with an initialized default branch and access for the configured bootstrap token.

This is not an unspecified external task: the hourly workflow observes the release condition and continues automatically when it becomes true.

## Canonical bootstrap files

The installer will create:

- `README.md`
- `STEGTRACE_MIRROR_HANDOFF.md`
- `CHANGELOG.md`
- `DISCLAIMER.md`
- `CONFIDENCE_LABELS.md`
- `docs/TRACE_OVERVIEW.md`
- `docs/TRACE_SIGNAL_BUNDLE.md`
- `docs/TRACE_PROFILES.md`
- `docs/TRACE_REEVALUATION_AND_DELTAS.md`
- `schemas/trace_signal_bundle.schema.json`
- `scripts/emit_bundle_example.py`
- `scripts/validate_trace.py`
- `.github/workflows/validate-trace.yml`

## Incomplete work after bootstrap

- Persistent immutable artifact store
- Versioned evaluation-record store
- Dependency/impact graph
- Calibrated confidence-vector engine
- Targeted reevaluation and delta generation
- StegTalk/trace adapter
- StegProv/trace adapter
- StegFREEDOM/trace adapter
- Cross-repository publication contracts and receipts

These tasks must be installed as target-repository issues or machine-readable task records after the bootstrap PR exists.

## Validation

Governance automation:

```bash
python -m py_compile scripts/bootstrap_stegtrace.py
```

Target bootstrap:

```bash
python scripts/validate_trace.py
```

Do not claim integration, release, or runtime activation from file creation alone. Inspect the target PR, workflow run, jobs, logs, and generated example bundle.

## Cross-repository dependencies

- Governance: consumer contract and GDR boundary
- StegCore: policy/runtime decisions informed by bounded TRACE signals
- StegTalk: ephemeral communication profile
- StegProv: persistent research profile
- StegFREEDOM: oversight profile
- Site, Publisher, admissibility-wiki, and stegguardian-wiki: propagation only after engine and profile claims are validated

## Completion measures

Bootstrap deliverables: 13 target files plus installer, workflow, receipt, handoff, issue, and pull request.

- Task completion: 6/10 current bootstrap milestones
- Developed-file completion: 3/4 Governance automation files installed; receipt is generated only at runtime
- Validation completion: static GitHub file installation complete; workflow execution pending merge
- Integration completion: 0/3 application profiles implemented
- Goal activation: target repository absent, so engine is not activated

## Permitted continuation scope

Future sessions and repository-native automation may merge PR #15 after checks pass, observe or create the target repository when authorized, execute the bootstrap installer, inspect the target PR and validation logs, and create target-owned runtime and profile tasks. They may not claim StegTrace runtime activation, publication propagation, or execution authority without corresponding repository evidence.

## Archive conditions

This temporary handoff is superseded when the target repository handoff is committed and the target validation workflow passes. Remaining work must then be represented by target-repository issues or task records with machine-observable completion evidence.
