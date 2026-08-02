# Relationship and Outcome Governance Mirror Handoff

## Repository

- Organization: `StegVerse-Labs`
- Repository: `Governance`
- Branch: `main`
- Layer: relationship formation, constructive participation, and outcome-direction governance

## Source of Truth

This file is the current handoff and task source of truth for the relationship and outcome governance layer. The repository-level `GOVERNANCE_MIRROR_HANDOFF.md` remains authoritative for shared Governance architecture and release boundaries.

## Determination

The layer was **partially present but not operationally complete**.

Previously present:

- a collaboration posture favoring overlap, bounded interoperability, and non-domination;
- human judgment, contestability, and legitimacy boundaries;
- repository-driven validation and continuation principles.

Previously absent:

- an explicit distinction among attention success, relationship effect, outcome direction, and continuation capacity;
- machine-readable tasks that always name their organization, repository, path, execution mode, and completion evidence;
- an automatic observer/executor that rejects unobservable `external` tasks;
- an evidence receipt exposing ready, blocked, completed, failed, and invalid work.

## Activation committed

The following files activate the initial layer:

```text
StegVerse-Labs/Governance:docs/governance/relationship_outcome_governance.md
StegVerse-Labs/Governance:automation/governance_task_registry.json
StegVerse-Labs/Governance:scripts/run_governance_tasks.py
StegVerse-Labs/Governance:.github/workflows/observe-governance-tasks.yml
StegVerse-Labs/Governance:docs/governance/RELATIONSHIP_OUTCOME_MIRROR_HANDOFF.md
```

The leading dot in `.github` may be omitted in user-facing workflow paths for readability, but the repository path retains it.

## Active tasks

### REL-OUTCOME-001

- Destination: `StegVerse-Labs/Governance:docs/governance/relationship_outcome_governance.md`
- Executor: `StegVerse-Labs/Governance:scripts/run_governance_tasks.py`
- Command: `python scripts/validate_docs.py`
- Completion evidence: `StegVerse-Labs/Governance:evidence/task-status/latest.json`

### REL-OUTCOME-002

- Destination: `StegVerse-Labs/Governance:automation/governance_task_registry.json`
- Executor: `StegVerse-Labs/Governance:scripts/run_governance_tasks.py`
- Command: `python scripts/run_governance_tasks.py --validate-only`
- Completion evidence: `StegVerse-Labs/Governance:evidence/task-status/latest.json`

### REL-OUTCOME-003

- Destination: `StegVerse-Labs/Governance:.github/workflows/observe-governance-tasks.yml`
- Observer: GitHub Actions on push, pull request, daily schedule, or recovery dispatch
- Completion condition: `StegVerse-Labs/Governance:evidence/task-status/latest.json` exists in the workflow artifact
- Artifact: `governance-task-status`

## Anti-halt rule

No task may remain as an unnamed external dependency.

Every task must be represented as one of:

1. `repository_command` — executable by a named script in a named repository;
2. `evidence_watch` — automatically observed against a named evidence condition;
3. `invalid` — rejected because its destination or completion condition is missing.

The runner fails closed for invalid or failed tasks. Blocked work remains visible in the receipt and is reevaluated by the scheduled workflow.

## Remaining build

1. Add canonical positive and negative fixtures for relationship-effect classification.
2. Add schema validation for governed outreach and collaboration commitments.
3. Integrate the layer with the existing GDR commitment-candidate mapping.
4. Publish task receipts durably rather than only as workflow artifacts.
5. Verify pertinent downstream representation in:
   - `StegVerse-Labs/Site`
   - `GCAT-BCAT-Engine/Publisher`
   - `StegVerse-Labs/admissibility-wiki`
   - `stegguardian-wiki` repository owner to be resolved from the connected installation before mutation.

## Definition of Done

The layer is fully activated when:

- its policy, schema, fixtures, validator, runner, workflow, and receipts are repository-resident;
- all relationship-effect cases are machine-tested;
- every active task has a repository destination and observable completion condition;
- blocked tasks are automatically re-observed;
- ready repository tasks execute without chat-only or human-memory dependency;
- downstream public surfaces accurately describe the layer and its authority boundaries.

## Completion assessment

```text
Conceptual architecture: complete
Repository-resident task registry: complete
Task validation: complete
Repository-command execution: complete
Evidence-watch observation: complete
Automatic workflow activation: complete
Canonical relationship fixtures: not yet built
Relationship commitment schema: not yet built
GDR integration: not yet built
Durable committed receipts: not yet built
Downstream publication: not yet verified
Manual continuation dependency: removed for registered tasks
```

## Permitted continuation scope

Future sessions may create the schema, fixtures, validator integration, receipt publication, and downstream synchronization directly in the named repositories. Prior conversation context is not required.
