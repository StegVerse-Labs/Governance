# Governance Task Observer Sovereign Mirror Handoff

Updated: 2026-08-19T01:05:00-05:00
Repository: `StegVerse-Labs/Governance`
Goal: `GOVERNANCE-SOVEREIGN-TASK-OBSERVER-001`

## Purpose

Replace the former hosted GitHub Actions Governance task executor/observer with a StegVerse-primary sovereign continuation that preserves Governance task-state observation without using GitHub-generated credentials as repository/runtime authority.

## Superseded hosted behavior

The former `.github/workflows/observe-governance-tasks.yml`:

- used `actions/checkout@v4` against the private repository;
- received a GitHub Actions token;
- declared `contents: write`;
- executed ready Governance repository tasks;
- generated task-state receipts;
- could commit and push those receipts;
- ran on push, pull request, schedule, and manual dispatch.

That surface is no longer admissible under the current TV/TVC-only credential policy. It has been reduced to a manual, zero-permission, non-checkout guard that performs no source execution or repository mutation.

Hosted guard success is not task observation, runtime proof, or activation.

## Implemented sovereign architecture

```text
Governance repository task registry
  -> existing TVC tvc.private-source-read.v1 exact read-only materialization
  -> canonical local StegVerse source/workload path
  -> central StegVerse WorkerCoordinator fresh claim/fence
  -> governance-sovereign-task-observer-worker
  -> local sovereign task-status / observer receipt
  -> bounded TVC repository-operation path only if persistence is separately admitted
```

The worker runs `scripts/run_governance_tasks.py` only from an exact already-materialized Governance source tree. It may not receive `GITHUB_TOKEN`, `GH_TOKEN`, PAT/provider/mailbox/wallet credentials, or any other NON-TV/TVC secret/token material.

The worker supports canonical local source discovery directly; WorkerCoordinator does not need to synthesize an environment binding. `STEGVERSE_GOVERNANCE_SOURCE_ROOT` is retained only as an optional non-secret explicit locator override.

Canonical local discovery includes user- and system-owned StegVerse source/workload paths such as:

```text
~/.stegverse/source/Governance
/var/lib/stegverse/source/Governance
~/.stegverse/workloads/Governance
/var/lib/stegverse/workloads/Governance
```

Lower-case `governance` equivalents and central-runtime workload paths are also supported. A candidate source root is accepted only when all required Governance files exist.

## Durable implementation bindings

Central StegVerse `.github`:

```text
worker:
  workers/governance_sovereign_task_observer_worker.py
handoff:
  handoffs/GOVERNANCE-SOVEREIGN-TASK-OBSERVER-001.json
registry fragment:
  control/worker-registry.d/governance-sovereign-task-observer-001.json
adapter:
  control/process-worker-adapters.d/governance-sovereign-task-observer-001.json
tests:
  tests/test_governance_sovereign_task_observer.py
source-validation receipt:
  docs/receipts/governance-sovereign-task-observer-source-validation-2026-08-19.json
canonical-discovery validation receipt:
  docs/receipts/governance-sovereign-task-observer-source-discovery-validation-2026-08-19.json
```

TVC source producer:

```text
parent capability task:
  StegVerse-Labs/TVC:tasks/TVC-PRIVATE-SOURCE-READ-001.json
consumer-specific handoff:
  StegVerse-Labs/TVC:docs/GOVERNANCE_SOURCE_MATERIALIZATION_MIRROR_HANDOFF.md
capability:
  tvc.private-source-read.v1
canonical issue:
  StegVerse-Labs/TVC#33
```

Governance is registered as a pending consumer of the existing TVC capability. No second credential broker, scheduler, source binder, or heartbeat path was created.

## Source validation evidence

Credential-clean exact-head validation established:

```text
observer source compile: PASS
canonical JSON parsing: PASS
executable handoff validation: PASS
AE exact effective denominator: PASS
explicit non-secret source locator: PASS
canonical local source discovery without env binding: PASS
incomplete local source candidate rejection: PASS
hosted environment rejection: PASS
GitHub token/PAT environment rejection: PASS
repository writeback authority rejection: PASS
heartbeat authority rejection: PASS
```

The validation runner explicitly proved `NO_GITHUB_CREDENTIAL_TOKEN_PRESENT`.

The broader central repository suite remains red on a separate pre-existing heartbeat-v12/state-transition semantic-debt cluster. Those legacy failures are not observer failures and do not become observer success by omission.

Source validation state:

```text
SOURCE_VALIDATED_BOUNDED_CANONICAL_DISCOVERY
```

This is not runtime proof.

## Authority boundary

```text
credential authority: TV/TVC ONLY
GitHub token runtime/repository authority: NONE
heartbeat grants execution authority: false
WorkerCoordinator is downstream observer/executor under separate admitted authority
Governance task observation grants no CGE authority
Governance task observation grants no architecture-decision authority
Governance task observation grants no transition authority
hosted GitHub Actions execution authority: NONE
repository writeback authority: NONE in observer
```

The independent heartbeat oscillator is unaffected by task state, source availability, observation state, source materialization, WorkerCoordinator claims, or this migration.

## Required runtime sequence

The remaining live path is now bounded and direct:

```text
1. TVC sole-host credential-admission owner observes the pending Governance consumer.
2. It re-resolves StegVerse-Labs/Governance refs/heads/main immediately before grant issuance.
3. It issues a <=900 second TV/TVC-only private-source-read request/grant bound to the exact re-resolved SHA, caller, source and consumer task.
4. scripts/private_source_read.py materializes the source read-only to a canonical local path and emits a secret-free materialization receipt.
5. WorkerCoordinator separately binds a collision-safe claim/fence to GOVERNANCE-SOVEREIGN-TASK-OBSERVER-001.
6. governance-sovereign-task-observer-worker discovers the local source and executes repository task observation with a stripped credential-free child environment.
7. The worker retains a local sovereign observer receipt.
8. CGE-DECISION-ISSUER-ARCHITECTURE-OWNERSHIP-001 remains blocked unless the actual architecture-decision receipt exists.
```

Materialization does not complete the observer task. Claim assignment does not complete it. Source validation does not complete it.

## Current state

```text
hosted observer/token authority: REMOVED_FROM_ACTIVE_EXECUTION_PATH
hosted schedule: REMOVED
hosted push/PR execution: REMOVED
hosted repository mutation: REMOVED
sovereign observer source: IMPLEMENTED
central worker registry binding: INSTALLED
central process adapter: INSTALLED
observer source validation: SOURCE_VALIDATED_BOUNDED_CANONICAL_DISCOVERY
TVC private-source consumer registration: INSTALLED
TVC consumer workflow validation this session: UNVALIDATED_NO_RUN
authority injection/grant issuance: NOT_OBSERVED
exact Governance source materialization: NOT_OBSERVED
WorkerCoordinator claim: NOT_OBSERVED
live sovereign observer execution: NOT_OBSERVED
live sovereign observation receipt: NOT_OBSERVED
migration state: BLOCKED_DEPENDENCY_MACHINE_OWNED
```

The absence of TVC workflow validation for the new consumer registration is preserved truthfully: TVC PR #82 produced no attached workflow run and was closed without merge. The parent private-source-read capability implementation remains separately established; this consumer binding is not promoted to workflow-validated state by inference.

## Downstream relationship

`CGE-DECISION-ISSUER-ARCHITECTURE-OWNERSHIP-001` remains a blocked Governance evidence-watch task. The sovereign observer is permitted to observe that task but cannot become the CGE issuer, Master Records authority, architecture-decision authority, or canonical transition executor.

Governance issue #19 remains the architecture-ownership decision surface for `MR.GAP.CGE_DECISION_ISSUER.001`.

## Failure policy

- exact source unavailable -> BLOCK on `TVC-PRIVATE-SOURCE-READ-001`;
- TV/TVC source materialization unavailable -> BLOCK;
- stale source SHA at grant time -> FAIL_CLOSED and re-resolve; do not reuse stale grant;
- any GitHub-generated or NON-TV/TVC credential requirement -> FAIL_CLOSED;
- worker cannot safely observe/repair -> submit the canonical sandbox-resolution successor task;
- missing architecture-decision receipt -> keep CGE architecture watch BLOCKED;
- hosted workflow success -> never substitute for sovereign observation;
- missing TVC consumer workflow run -> remain `UNVALIDATED_NO_RUN`, not PASS.

## Execution ownership and collision partition

### MANUAL / SESSION-STARTABLE

No direct Governance task execution is manually startable from hosted Actions.

### WORKER-OWNED / DO NOT COMPETE

```yaml
- task_id: GOVERNANCE-SOVEREIGN-TASK-OBSERVER-001
  execution_owner: central StegVerse WorkerCoordinator / governance-sovereign-task-observer-worker
  claim_state: HANDOFF_READY
  worker_registry_ref: StegVerse-Labs/.github:control/worker-registry.d/governance-sovereign-task-observer-001.json
  manual_execution_allowed: false
  manual_allowed_role: observation and source/evidence review only
  collision_scope: Governance task-registry observation and sovereign task-status receipt production
  release_condition: TV/TVC exact Governance materialization is present, WorkerCoordinator binds a fresh claim/fence, and the worker produces a credential-clean sovereign observer receipt
  next_executable_action: existing TVC credential-admission/sole-host owner materializes the current exact Governance source; then WorkerCoordinator claims and executes the already-validated observer
```

### ESCALATED / AUTHORITY-OWNED

Credential-bearing private-source materialization or repository persistence remains TV/TVC-owned. Actual CGE/Master Records decision issuance remains unresolved under Governance #19 / StegDB `MR.GAP.CGE_DECISION_ISSUER.001`.

### COMPLETED / SUPERSEDED

The former hosted scheduled/push/PR task execution and receipt-push behavior is superseded and must not be restored as production continuation.

## Completion

This migration completes only when the implemented sovereign observer executes under a fresh WorkerCoordinator claim with exact TV/TVC-materialized source and produces durable sovereign task-state evidence. Source implementation, source validation, consumer registration, handoff readiness, or hosted guard success is not completion.
