# Governance Task Observer Sovereign Mirror Handoff

Updated: 2026-08-19T00:02:00-05:00
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

## Target sovereign architecture

```text
Governance repository task registry
  -> TV/TVC-controlled exact source materialization or already-local source
  -> central StegVerse WorkerCoordinator fresh claim/fence
  -> credential-clean Governance task observer
  -> repository-local task-status receipt
  -> bounded TVC repository-operation path if persistence is separately admitted
```

The worker must run `scripts/run_governance_tasks.py` only from exact locally materialized Governance source. It may not receive `GITHUB_TOKEN`, `GH_TOKEN`, provider credentials, mailbox credentials, wallet credentials, or other NON-TV/TVC secret/token material.

## Authority boundary

```text
credential authority: TV/TVC ONLY
GitHub token runtime/repository authority: NONE
heartbeat grants execution authority: false
WorkerCoordinator is downstream observer/executor under separate admitted authority
Governance task observation grants no CGE authority
Governance task observation grants no transition authority
hosted GitHub Actions execution authority: NONE
```

The independent heartbeat oscillator is unaffected by task state, source availability, observation state, or this migration.

## Required capabilities

The future sovereign worker requires only:

- exact local Governance source discovery/materialization;
- bounded process execution;
- Governance task-registry validation;
- task-state observation;
- receipt creation inside its allowed sandbox/output scope;
- no direct credential-bearing repository mutation.

Any persistence back into the private Governance repository must use a separately admitted TVC repository-operation capability and cannot be inferred from task completion.

## Current state

```text
hosted observer/token authority: REMOVED_FROM_ACTIVE_EXECUTION_PATH
hosted schedule: REMOVED
hosted push/PR execution: REMOVED
hosted repository mutation: REMOVED
sovereign observer source: NOT_YET_IMPLEMENTED
central worker registry binding: NOT_YET_INSTALLED
TVC source/persistence path: REQUIRED_SEPARATE_ADMISSION
live sovereign observation receipt: NOT_OBSERVED
```

## Downstream relationship

`CGE-DECISION-ISSUER-ARCHITECTURE-OWNERSHIP-001` remains a blocked Governance evidence-watch task. The sovereign observer should eventually observe that task without becoming the CGE issuer or architecture decision authority.

## Failure policy

- exact source unavailable -> BLOCK;
- TV/TVC source materialization unavailable -> BLOCK;
- any GitHub/generated or NON-TV/TVC credential requirement -> FAIL_CLOSED;
- worker cannot safely observe/repair -> submit sandbox-resolution task;
- missing architecture-decision receipt -> keep CGE architecture watch BLOCKED;
- hosted workflow success -> never substitute for sovereign observation.

## Execution ownership and collision partition

### MANUAL / SESSION-STARTABLE

No direct Governance task execution is manually startable from hosted Actions.

### WORKER-OWNED / DO NOT COMPETE

```yaml
- task_id: GOVERNANCE-SOVEREIGN-TASK-OBSERVER-001
  execution_owner: future central StegVerse WorkerCoordinator / Governance observer worker
  claim_state: HANDOFF_READY_AFTER_REGISTRATION
  worker_registry_ref: future StegVerse-Labs/.github control/worker-registry.d/governance-sovereign-task-observer-001.json
  manual_execution_allowed: false
  manual_allowed_role: observation and source/evidence review only
  collision_scope: Governance task-registry observation and task-status receipt production
  release_condition: central sovereign worker binding exists and produces a credential-clean task-status receipt from exact Governance source
  next_executable_action: install the bounded central worker/adapter/handoff without reactivating hosted GitHub credential authority
```

### ESCALATED / AUTHORITY-OWNED

Credential-bearing private-source materialization or repository persistence remains TV/TVC-owned.

### COMPLETED / SUPERSEDED

The former hosted scheduled/push/PR task execution and receipt-push behavior is superseded and must not be restored as production continuation.

## Completion

This migration completes only when the sovereign observer is implemented, registered, validated, executes under a fresh WorkerCoordinator claim with credential-clean exact source, and produces durable task-state evidence. Source installation or hosted guard success is not completion.
