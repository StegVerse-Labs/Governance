# Governance Mirror Handoff

## Repository

- Organization: StegVerse-Labs
- Repository: Governance
- Current goal: continue building without manual actions needed through completion OR until task handoff and task completion is capable of being handled by the ecosystem's own management.
- Current activation target: preserve governance policy, canonical fixtures, validation, ingestion, ownership, and cross-repository runtime alignment without prior chat context or manual-only verification.

## Source of Truth

This file is the current handoff and task source of truth for Governance work.

Continue from this file before changing governance docs, fixtures, validators, workflows, indexes, or integration contracts.

## Current Build State

The repository contains:

1. constitutional, dual-quorum, drift, anchoring, identity, lifecycle, economic, registry, and citizenship governance drafts;
2. indexed documentation and deferred-review tracking;
3. reusable, inbox-driven conversation ingestion with automatic smoke testing;
4. push- and pull-request-driven documentation and fixture validation;
5. the judgment, signal formation, and execution architecture;
6. GDR schema mapping for the three-layer contract;
7. three negative fixtures;
8. one positive-control fixture;
9. a replay pair preserving policy and authority while changing admitted signals and reference state;
10. runtime expectations aligned to StegCore;
11. validator enforcement of shape, outcomes, replay invariants, and `continuity_receipt_minted=false`;
12. live StegCore cross-repository verification on push, pull request, and daily schedule;
13. automated StegCore evidence publication and issue closure.

## Required Three-Layer Files

```text
docs/governance/judgment_signal_execution_architecture.md
docs/examples/GDR_SCHEMA_MAPPING.md
docs/examples/fixtures/condition_degraded_judgment_gdr.json
docs/examples/fixtures/signal_admission_drift_gdr.json
docs/examples/fixtures/governance_validation_of_drift_gdr.json
docs/examples/fixtures/three_layer_positive_control_gdr.json
docs/examples/fixtures/three_layer_replay_baseline_gdr.json
docs/examples/fixtures/three_layer_replay_mutated_gdr.json
scripts/validate_gdr_examples.py
scripts/validate_docs.py
scripts/ingest_conversation.py
scripts/test_ingest_conversation.py
.github/workflows/validate_docs.yml
.github/workflows/ingest_conversation.yml
docs/ACTIVATION_STATUS.md
```

Note: when presenting workflow paths to the user, display them without the leading dot and state that it was omitted for readability.

## Durable Decision

Human judgment remains essential to meaning, context, purpose, contestability, and legitimacy. Governance must separately preserve:

1. conditions supporting meaningful human judgment;
2. integrity of signal admission and state formation;
3. commit-time execution admissibility.

Human approval alone does not repair degraded judgment conditions, incomplete state formation, or shifted reference-state continuity.

## Canonical Runtime Cases

- Condition-degraded judgment: `DENY` with `judgment.refusal_unavailable`.
- Incomplete or unreconstructable signal admission: `DENY` with `signal.inputs_incomplete`.
- Valid policy and authority over a shifted reference state: `FAIL-CLOSED` with `signal.reference_state_discontinuous`.
- Complete positive control: `ALLOW` with `ok`.
- Replay baseline: `ALLOW`.
- Replay mutation with unchanged policy, authority, and delegation but changed admitted signals and reference state: `FAIL-CLOSED`.

All canonical runtime expectations require `continuity_receipt_minted=false`.

## Cross-Repository Automation

`StegVerse-Labs/StegCore` owns runtime implementation under issue #22.

StegCore:

- implements the three-layer evaluator;
- tests negative, positive, replay, and non-minting behavior;
- clones Governance during CI;
- evaluates all six canonical fixtures through the actual runtime;
- repeats the contract check daily;
- writes passing evidence to `evidence/runtime-validation.json`;
- commits evidence only when the validated StegCore or Governance contract commit changes;
- closes issue #22 automatically after every required gate passes.

## Evidence Consumption Rule

Governance consumes StegCore runtime evidence by reference to:

```text
StegVerse-Labs/StegCore/evidence/runtime-validation.json
```

The evidence record must identify the Governance commit it validated. This handoff does not require copied workflow IDs, copied console output, or a manually edited pass declaration.

A Governance commit is runtime-aligned only when the StegCore evidence record has:

- `status: pass`;
- `governance_commit` equal to that canonical Governance contract commit;
- all required checks marked as passing;
- `continuity_receipt_minted: false`;
- all authority non-claims preserved.

## Active Ownership

- Governance architecture, schema mapping, canonical fixtures, and validation contract: `StegVerse-Labs/Governance`.
- Runtime evaluator, runtime receipt, tests, live verifier, evidence record, and issue closure: `StegVerse-Labs/StegCore`.
- Continuity receipt verification or minting: outside Governance and StegCore authority.
- Legal, employment, medical, biometric, or human-performance measurement policy: outside current scope and requires separate review.

## Manual Tasks Eliminated

- Conversation-ingestion smoke testing is automatic.
- Repository inbox ingestion is push-driven.
- Fixture presence, field shape, expected outcomes, replay invariants, and receipt boundaries are machine-enforced.
- Governance-to-StegCore alignment is checked against live fixtures.
- Daily scheduled verification detects later drift.
- Passing runtime evidence is generated and committed automatically.
- Governance consumes evidence through a durable pointer rather than manual transcription.
- Issue #22 closes automatically only after all runtime gates pass.
- Manual workflow dispatch remains only as a recovery option.

## Next Actions

1. Allow Governance validation to continue automatically.
2. Allow the first successful StegCore non-PR validation to publish `evidence/runtime-validation.json` and close issue #22.
3. Correct failures through repository commits without manual execution or evidence copying.
4. After passing evidence exists, apply the release-readiness gate.
5. Tag or release only after evidence validity, version uniqueness, authority boundaries, and downstream task declarations pass.
6. At release readiness, verify applicable updates to Site, Publisher, admissibility-wiki, and stegguardian-wiki.

## Definition of Done

The Governance side is complete when:

- all architecture and fixture records are repository-resident;
- validators enforce all six canonical cases;
- validation runs automatically;
- StegCore evaluates the canonical fixtures live;
- Governance consumes passing StegCore evidence by commit-bound reference;
- both repositories preserve ownership and authority boundaries;
- future continuation requires no original chat or manual-only action.

Full runtime activation additionally requires the automatically generated StegCore evidence record and automated issue #22 closure.

## Current Completion Assessment

```text
Governance architecture: complete
Schema mapping: complete
Negative fixtures: complete
Positive fixture: complete
Replay fixtures: complete
Fixture validator: complete
Ingestion automation: complete
Live StegCore contract integration: complete
Automated evidence consumption rule: complete
Passing evidence record: pending first successful StegCore non-PR run
Manual continuation dependency: none
```

## Archive Status

This conversation's unique decisions, fixtures, implementation boundaries, automation, evidence mechanics, ownership, remaining gates, and continuation scope are durably recorded. The thread is ready for archive.
