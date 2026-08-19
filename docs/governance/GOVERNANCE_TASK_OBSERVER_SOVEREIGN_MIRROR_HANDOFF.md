# Governance Task Observer Sovereign Mirror Handoff

Updated: 2026-08-19T07:24:00-05:00
Repository: `StegVerse-Labs/Governance`
Goal: `GOVERNANCE-SOVEREIGN-TASK-OBSERVER-001`

## Purpose

Replace the former hosted GitHub Actions Governance task executor/observer with a StegVerse-primary sovereign continuation that preserves Governance task-state observation without using GitHub-generated credentials as repository/runtime authority.

## Superseded hosted behavior

The former `.github/workflows/observe-governance-tasks.yml` used hosted checkout/token authority, executed Governance tasks, persisted task-state receipts, and could commit/push those receipts. That production continuation has been removed. The remaining hosted surface is validation/guard evidence only and grants no runtime or repository authority.

Hosted guard success is not task observation, runtime proof, activation, or release.

## Implemented sovereign architecture

```text
Governance task registry
  -> TVC tvc.private-source-read.v1 credential-admission owner
  -> scripts/execute_private_source_read_consumer.py
       resolve current ref
       -> create fresh in-memory <=900s request
       -> grant issuance with ref re-resolution
       -> exact materialization with ref re-resolution
       -> secret-free execution receipt
  -> canonical local StegVerse Governance source path
  -> non-authorizing heartbeat assignment packet
  -> WorkerCoordinator authorization/reconstruction/budget/worker checks
  -> fresh claim/fence
  -> governance-sovereign-task-observer-worker
  -> ProcessWorkerAdapter fenced bound-state projection
       observed/latest.json
       receipts/latest.json
```

No source-binding worker, second scheduler, extra heartbeat path, GitHub Actions runtime executor, or second credential broker is required.

## Canonical local source discovery

The observer consumes only already-materialized exact Governance source. It supports an optional non-secret `STEGVERSE_GOVERNANCE_SOURCE_ROOT` locator and canonical StegVerse local paths including:

```text
~/.stegverse/source/Governance
/var/lib/stegverse/source/Governance
~/.stegverse/workloads/Governance
/var/lib/stegverse/workloads/Governance
```

Lower-case equivalents and central-runtime workload paths are also supported. A candidate is accepted only when the canonical Governance handoff, task registry, observer script, and CGE architecture handoff all exist.

## Durable implementation bindings

Central `StegVerse-Labs/.github`:

```text
worker:
  workers/governance_sovereign_task_observer_worker.py
executable handoff:
  handoffs/GOVERNANCE-SOVEREIGN-TASK-OBSERVER-001.json
registry fragment:
  control/worker-registry.d/governance-sovereign-task-observer-001.json
adapter:
  control/process-worker-adapters.d/governance-sovereign-task-observer-001.json
least-privilege profile:
  control/worker-capability-profiles.json#governance-sovereign-observer-v1
finite cost basis:
  cost-basis/worker-runtime/governance-sovereign-task-observer.json
tests:
  tests/test_governance_sovereign_task_observer.py
validation receipts:
  docs/receipts/governance-sovereign-task-observer-source-validation-2026-08-19.json
  docs/receipts/governance-sovereign-task-observer-source-discovery-validation-2026-08-19.json
  docs/receipts/governance-sovereign-task-observer-runtime-contract-validation-2026-08-19.json
```

TVC source producer:

```text
capability task:
  StegVerse-Labs/TVC:tasks/TVC-PRIVATE-SOURCE-READ-001.json
canonical handoff:
  StegVerse-Labs/TVC:docs/PRIVATE_SOURCE_READ_MIRROR_HANDOFF.md
Governance consumer handoff:
  StegVerse-Labs/TVC:docs/GOVERNANCE_SOURCE_MATERIALIZATION_MIRROR_HANDOFF.md
machine executor:
  StegVerse-Labs/TVC:scripts/execute_private_source_read_consumer.py
executor tests:
  StegVerse-Labs/TVC:tests/test_execute_private_source_read_consumer.py
capability:
  tvc.private-source-read.v1
issue:
  StegVerse-Labs/TVC#33
```

## Observer runtime-contract validation

Credential-clean exact-head validation now proves the actual WorkerCoordinator + ProcessWorkerAdapter path rather than only the internal worker function.

```text
Governance observer tests: 10/10 PASS
anonymous checkout without GitHub credential token: PASS
compile: PASS
canonical JSON parsing: PASS
executable-handoff validation: PASS
unique WorkerCoordinator worker selection: PASS
finite 16-unit cost basis: PASS
least-privilege capability profile: PASS
bound-state adapter scope observed/** + receipts/**: PASS
missing source -> HANDOFF_READY without duplicate resolution task: PASS
real observer defect -> valid sandbox-resolution contract: PASS
COMPLETED response + transition sequence: PASS
hosted execution rejection: PASS
GitHub token environment rejection: PASS
repository writeback authority rejection: PASS
heartbeat execution-authority rejection: PASS
CGE watch requires actual architecture-decision receipt: PASS
```

Exact retained state:

```text
SOURCE_VALIDATED_BOUNDED_RUNTIME_CONTRACT
```

The validation workflow as a whole remains red only because of a separate pre-existing heartbeat/state-transition compatibility cluster (10 failures / 16 errors in the 444-test repository suite). Those failures are not Governance-observer failures and are not hidden.

## TVC executor state

The TVC machine lane now has a concrete generic executor instead of an instruction-only transition from credential admission to the low-level materializer.

The executor:

- requires TV/TVC injection at execution time and acquires no credential itself;
- emits `BLOCKED_DEPENDENCY` with no fallback when injection is absent;
- creates the request in memory only after resolving the current tracked ref;
- re-resolves during grant issuance and again during materialization;
- defaults to 600s and rejects TTL >900s;
- never places the credential in arguments or receipts;
- may idempotently reuse an existing checkout only if local HEAD equals the currently resolved exact SHA;
- refuses implicit deletion/replacement of a different occupied destination;
- grants no write/release/publication/runtime/production authority.

Its deterministic tests are installed in TVC, but TVC validation-only PR #85 received **no Actions run** even with a `tests/**` change. Therefore:

```text
TVC machine executor source: IMPLEMENTED
TVC machine executor hosted validation: UNVALIDATED_NO_RUN
TVC authority injection: NOT_OBSERVED
TVC grant activation: NOT_OBSERVED
exact Governance materialization: NOT_OBSERVED
```

No PASS is inferred from the no-run condition.

## Observer process semantics

Missing exact local Governance source is not represented as a `BLOCKED` worker defect. The observer returns:

```text
HANDOFF_READY / GOVERNANCE_SOURCE_MATERIALIZATION_PENDING
```

This releases the claim and preserves `TVC-PRIVATE-SOURCE-READ-001` as the existing source owner instead of manufacturing a duplicate resolution task.

A real internal observer/runtime defect returns `BLOCKED` with a machine-readable resolution contract. If the assigned worker cannot repair it, the canonical runtime derives the sandbox-resolution successor with `repository_resolution` + `sandbox_validation`; no generic retry/credential fallback is substituted.

Successful observation returns `COMPLETED` only after registry validation and CGE-watch predicates pass.

## Fenced local state

The observer no longer writes directly to host `HOME`. The adapter uses:

```text
process_json_bound_state_v0.1
bound_state_root:
  ~/.stegverse/state/governance-sovereign-task-observer
allowed relative paths:
  observed/**
  receipts/**
```

The worker sees only a sandbox-local `STEGVERSE_BOUND_STATE_ROOT`; the authoritative host path is not exposed. State changes are projected only after current claim/fence and path-scope validation.

## Authority boundary

```text
credential authority: TV/TVC ONLY
GitHub token runtime/repository authority: NONE
heartbeat grants execution authority: false
assignment packet grants execution authority: false
capability profile grants authority: false
worker availability grants authority: false
Governance repository writeback authority: false
CGE decision authority: false
architecture-decision authority: false
release/deployment authority: false
```

The independent heartbeat oscillator progresses at its canonical 10ms reference cadence regardless of source availability, task state, claims, WorkerCoordinator activity, TVC injection, or observer execution. This lane never causes or gates heartbeat progression.

## Required live sequence

```text
1. Existing TVC credential-admission/sole-host owner gets a genuine TV/TVC private-source injection opportunity.
2. It invokes scripts/execute_private_source_read_consumer.py for the Governance pending consumer.
3. Executor resolves then-current StegVerse-Labs/Governance refs/heads/main.
4. It creates a fresh <=900s request, issues the policy-bound grant, re-resolves, materializes, re-resolves, and emits secret-free exact-source evidence.
5. Governance source is present at a canonical local path.
6. Heartbeat may carry a non-authorizing assignment packet; heartbeat itself grants nothing.
7. WorkerCoordinator separately rechecks execution authorization, lineage/reconstruction, finite budget, profile/capability match, unique AVAILABLE worker, then binds a fresh claim/fence.
8. ProcessWorkerAdapter invokes the observer in its fenced sandbox/bound-state envelope.
9. Observer validates the Governance task registry and CGE watch, then returns COMPLETED with fenced evidence.
10. CGE-DECISION-ISSUER-ARCHITECTURE-OWNERSHIP-001 remains blocked unless its actual architecture-decision receipt exists.
```

Materialization does not complete the observer. Assignment does not complete it. Claiming does not complete it. Source/runtime-contract validation does not complete it.

## Current state

```text
hosted observer/token authority: REMOVED_FROM_ACTIVE_EXECUTION_PATH
sovereign observer implementation: COMPLETE_SOURCE
executable handoff: INSTALLED
registry binding: INSTALLED
least-privilege profile: INSTALLED
finite cost basis: INSTALLED
bound-state adapter: INSTALLED
observer runtime contract: SOURCE_VALIDATED_BOUNDED_RUNTIME_CONTRACT
TVC generic machine executor: IMPLEMENTED
TVC generic machine executor hosted validation: UNVALIDATED_NO_RUN
TVC authority injection: NOT_OBSERVED
exact Governance source materialization: NOT_OBSERVED
WorkerCoordinator live claim/fence: NOT_OBSERVED
sovereign observer live execution: NOT_OBSERVED
sovereign observer live receipt: NOT_OBSERVED
CGE architecture decision receipt: NOT_OBSERVED
migration state: BLOCKED_DEPENDENCY_MACHINE_OWNED
```

## Execution ownership and collision partition

### MANUAL / SESSION-STARTABLE

Hosted/manual Actions are not a production execution path. This session may inspect and improve source/contract evidence but may not invent or expose credential values.

### MACHINE-OWNED / DO NOT COMPETE

```yaml
- source_task: TVC-PRIVATE-SOURCE-READ-001
  owner: TVC credential_admission / sole-host StegVerse control plane
  executor: scripts/execute_private_source_read_consumer.py
  release_condition: secret-free exact Governance materialization receipt under a current TV/TVC grant

- task_id: GOVERNANCE-SOVEREIGN-TASK-OBSERVER-001
  owner: central WorkerCoordinator / governance-sovereign-task-observer-worker
  state: HANDOFF_READY
  manual_execution_allowed: false
  release_condition: exact local source + fresh claim/fence + COMPLETED observer receipt
```

### ESCALATED / AUTHORITY-OWNED

Actual CGE/Master Records decision issuance remains unresolved under Governance #19 / `MR.GAP.CGE_DECISION_ISSUER.001`.

## Failure policy

- missing TVC injection -> remain machine-owned dependency; no generic credential fallback;
- stale source ref/SHA -> fail closed and re-resolve;
- occupied different materialization destination -> fail closed; no implicit destructive replacement;
- missing local source at observer invocation -> HANDOFF_READY and release claim; do not duplicate TVC ownership;
- real observer defect -> BLOCKED with resolution contract;
- unable/impossible observer repair -> sandbox-resolution successor;
- missing CGE architecture decision receipt -> keep CGE watch blocked;
- hosted workflow/no-run condition -> never substitute for live proof.

## Completion

This migration completes only when the already-built observer consumes exact TV/TVC-materialized Governance source under a fresh WorkerCoordinator claim/fence and emits its fenced sovereign task-state receipt. The TVC machine executor must first be source-validated through the strongest available path and then actually execute under real TV/TVC authority. None of those live predicates have yet occurred.

`DO NOT ARCHIVE THIS SESSION — REQUIRED MACHINE EXECUTION REMAINS.`
