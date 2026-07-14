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

The repository now contains:

1. constitutional, dual-quorum, drift, anchoring, identity, lifecycle, economic, registry, and citizenship governance drafts;
2. indexed documentation and deferred-review tracking;
3. reusable, inbox-driven conversation ingestion with automatic smoke testing;
4. push- and pull-request-driven documentation and fixture validation;
5. the judgment, signal formation, and execution architecture;
6. GDR schema mapping for the three-layer contract;
7. three negative fixtures;
8. one positive-control fixture;
9. a two-part replay fixture preserving policy/authority while changing admitted signals and reference state;
10. runtime expectations aligned to the StegCore evaluator;
11. validator enforcement of fixture shape, outcomes, replay invariants, and `continuity_receipt_minted=false`;
12. live StegCore cross-repository fixture verification on push, pull request, and daily schedule.

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
- Valid policy/authority over a shifted reference state: `FAIL-CLOSED` with `signal.reference_state_discontinuous`.
- Complete positive control: `ALLOW` with `ok`.
- Replay baseline: `ALLOW`.
- Replay mutation with unchanged policy, authority, and delegation but changed admitted signals/reference state: `FAIL-CLOSED`.

All canonical runtime expectations require `continuity_receipt_minted=false`.

## Cross-Repository Automation

`StegVerse-Labs/StegCore` owns runtime implementation under issue #22.

StegCore now:

- implements the three-layer evaluator;
- tests negative, positive, replay, and non-minting behavior;
- clones Governance during CI;
- evaluates all six canonical fixtures through the actual runtime;
- repeats the contract check daily to detect future drift without manual initiation.

## Active Ownership

- Governance architecture, schema mapping, canonical fixtures, and validation contract: `StegVerse-Labs/Governance`.
- Runtime evaluator, runtime receipt, tests, and live cross-repository verifier: `StegVerse-Labs/StegCore` issue #22.
- Continuity receipt verification or minting: outside Governance and StegCore authority.
- Legal, employment, medical, biometric, or human-performance measurement policy: outside current scope and requires separate review.

## Manual Tasks Eliminated

- Conversation-ingestion smoke testing is automatic.
- Repository inbox ingestion is push-driven.
- Fixture presence, field shape, expected outcomes, replay invariants, and receipt boundaries are machine-enforced.
- Runtime placement and result vocabulary are durably assigned.
- Governance-to-StegCore alignment is checked against live fixtures rather than manual comparison.
- Daily scheduled verification detects later cross-repository drift.
- Manual workflow dispatch remains only as a recovery option.

## Next Actions

1. Capture passing Governance validation evidence.
2. Capture passing StegCore runtime and live-contract evidence.
3. Correct failures through repository commits without requiring manual-only execution.
4. Record passing commit/run evidence in this handoff, the StegCore handoff, and issue #22.
5. Close issue #22 only after automated evidence passes.
6. Perform release-readiness and tagging only after all gates pass.
7. At release readiness, verify applicable updates to Site, Publisher, admissibility-wiki, and stegguardian-wiki.

## Definition of Done

The Governance side is complete when:

- all architecture and fixture records are repository-resident;
- validators enforce all six canonical cases;
- validation runs automatically;
- StegCore evaluates the canonical fixtures live;
- both repositories preserve ownership and authority boundaries;
- future continuation requires no original chat or manual-only action.

Full runtime activation additionally requires passing workflow evidence and release-boundary recording.

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
Passing workflow evidence: pending
Manual continuation dependency: none
```

## Archive Status

This conversation's unique decisions, fixtures, implementation boundaries, automation, ownership, remaining gates, and continuation scope are durably recorded. The thread is ready for archive.
