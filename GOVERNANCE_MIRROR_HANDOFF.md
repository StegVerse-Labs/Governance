# Governance Mirror Handoff

## Repository

- Organization: StegVerse-Labs
- Repository: Governance
- Current goal: continue building without manual actions needed through completion OR until task handoff and task completion is capable of being handled by the ecosystem's own management.
- Current activation target: preserve governance policy, canonical fixtures, validation, ingestion, ownership, cross-repository runtime alignment, and bounded external-evidence interoperability without prior chat context or manual-only verification.

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
7. three negative fixtures, one positive-control fixture, and one replay pair;
8. runtime expectations aligned to StegCore;
9. validator enforcement of shape, outcomes, replay invariants, and `continuity_receipt_minted=false`;
10. live StegCore cross-repository verification and automated evidence publication;
11. a durable accountability-stack interoperability position;
12. a machine-readable external evidence-provider interface contract;
13. five canonical external-evidence fixtures covering valid, stale, drifted, incomplete, and unauthorized-provider cases;
14. CI validation of external-evidence shape, expected outcomes, replay invariants, non-minting, and provider non-authority.

## Required Files

```text
docs/governance/judgment_signal_execution_architecture.md
docs/governance/ACCOUNTABILITY_STACK_INTEROP_POSITION.md
docs/examples/GDR_SCHEMA_MAPPING.md
docs/examples/EXTERNAL_EVIDENCE_PROVIDER_INTERFACE.md
docs/examples/fixtures/condition_degraded_judgment_gdr.json
docs/examples/fixtures/signal_admission_drift_gdr.json
docs/examples/fixtures/governance_validation_of_drift_gdr.json
docs/examples/fixtures/three_layer_positive_control_gdr.json
docs/examples/fixtures/three_layer_replay_baseline_gdr.json
docs/examples/fixtures/three_layer_replay_mutated_gdr.json
docs/examples/interop/external_evidence_valid.json
docs/examples/interop/external_evidence_stale.json
docs/examples/interop/external_evidence_drifted.json
docs/examples/interop/external_evidence_incomplete.json
docs/examples/interop/external_evidence_unauthorized.json
scripts/validate_gdr_examples.py
scripts/validate_external_evidence_interop.py
scripts/validate_docs.py
scripts/ingest_conversation.py
scripts/test_ingest_conversation.py
.github/workflows/validate_docs.yml
.github/workflows/ingest_conversation.yml
docs/ACTIVATION_STATUS.md
```

When presenting workflow paths to the user, omit the leading dot for readability and state that it was omitted.

## Durable Governance Decision

Human judgment remains essential to meaning, context, purpose, contestability, and legitimacy. Governance separately preserves:

1. conditions supporting meaningful human judgment;
2. integrity of signal admission and state formation;
3. commit-time execution admissibility.

Human approval alone does not repair degraded judgment conditions, incomplete state formation, shifted reference-state continuity, stale evidence, or unauthorized evidence production.

## Accountability-Stack Collaboration Decision

StegVerse prefers collaboration where independent accountability architectures overlap, while allowing differentiation to emerge from the areas each system can independently master.

Differentiation is not used to dominate or displace another architecture. Out-execution remains a work-product outcome rather than the governing strategy.

StegVerse already provides implemented constitutional machinery through canonical cases, machine-enforced validation, replay, drift detection, runtime evaluation, evidence publication, ownership boundaries, and fail-closed outcomes.

The active goal is to strengthen evidence interfaces and demonstrate bounded interoperability with complementary telemetry, attestation, and verification systems without collapsing proof into authority, admissibility, execution, custody, or adjudication.

## Canonical Runtime Cases

Original three-layer cases:

- degraded judgment: `DENY / judgment.refusal_unavailable`;
- incomplete signal admission: `DENY / signal.inputs_incomplete`;
- shifted reference state: `FAIL-CLOSED / signal.reference_state_discontinuous`;
- positive control: `ALLOW / ok`;
- replay baseline: `ALLOW`;
- replay mutation: `FAIL-CLOSED`.

External evidence cases:

- valid evidence: `ALLOW / ok`;
- stale evidence: `DENY / evidence.stale`;
- drifted reference state: `FAIL-CLOSED / evidence.reference_state_drift`;
- incomplete evidence: `DENY / evidence.incomplete`;
- unauthorized provider: `DENY / evidence.provider_unauthorized`.

Every case requires:

```text
continuity_receipt_minted: false
evidence_provider_execution_authority: false
```

The second field applies to external-evidence fixtures. Evidence integrity, signature validity, or successful verification never grants execution authority.

## External Evidence Mapping Boundary

The external envelope binds provider identity, provider type, subject, capture interval, execution context, claims, evidence digests, chain posture, authorization, freshness, reference state, and prior-hash linkage.

It maps into a commitment candidate containing actor, target, scope, action, execution context, policy, delegation, consent, identity, evidence, validity, reference state, recoverability, and provider authorization references.

The mapper and Governance contract do not grant:

- execution authority;
- Master-Records custody;
- legal adjudication;
- insurance acceptance;
- regulatory recognition;
- Continuity receipt verification or minting.

## Cross-Repository Automation

`StegVerse-Labs/StegCore` owns runtime implementation under issue #22 for the original three-layer evaluator and its evidence publication.

Governance now owns the external evidence-provider interface, canonical interop fixtures, and repository-side validator. StegCore runtime support for the five external-evidence cases is the next cross-repository integration task and must preserve all non-authority and non-minting boundaries.

Governance consumes StegCore runtime evidence by reference to:

```text
StegVerse-Labs/StegCore/evidence/runtime-validation.json
```

A Governance commit is runtime-aligned only when the evidence record identifies that Governance commit, reports `status: pass`, marks all required checks passing, preserves `continuity_receipt_minted: false`, and retains all authority non-claims.

## Active Ownership

- Governance architecture, schemas, canonical fixtures, validators, collaboration posture, and external evidence contract: `StegVerse-Labs/Governance`.
- Runtime evaluator, runtime receipts, tests, live verifier, and evidence publication: `StegVerse-Labs/StegCore`.
- External telemetry, attestation, and verification providers retain ownership of their evidence-producing systems and claims.
- Continuity receipt verification or minting: outside Governance and StegCore authority.
- Master-record custody, legal adjudication, insurance acceptance, regulatory recognition, and deployment authority: separate scopes.
- Legal, employment, medical, biometric, or human-performance measurement policy: outside current scope and requires separate review.

## Manual Tasks Eliminated

- Conversation-ingestion smoke testing is automatic.
- Repository inbox ingestion is push-driven.
- Original GDR fixture shape, outcomes, replay invariants, and receipt boundaries are machine-enforced.
- External evidence fixture shape, outcomes, authorization, freshness, reference-state drift, non-minting, and provider non-authority are machine-enforced.
- Governance validation runs on push and pull request.
- Governance-to-StegCore alignment is checked against live fixtures for the established runtime contract.
- Daily verification detects later drift.
- Passing runtime evidence is generated and committed automatically for the established runtime contract.
- Manual workflow dispatch remains only as a recovery option.

## Remaining Work

```text
StegVerse-Labs/Governance
  -> observe Validate Governance Docs on current main
  -> repair only exact validator failures without weakening invariants
  -> keep external evidence schema and canonical fixtures authoritative

StegVerse-Labs/StegCore
  -> ingest external evidence envelope version 1.0
  -> map it into the existing commit-time evaluator
  -> implement ALLOW, DENY, and FAIL-CLOSED behavior for all five cases
  -> test stale, drifted, incomplete, and unauthorized-provider rejection
  -> preserve evidence_provider_execution_authority=false
  -> preserve continuity_receipt_minted=false
  -> publish commit-bound runtime evidence for the Governance contract

Release propagation after readiness
  -> verify pertinent updates to StegVerse-Labs/Site
  -> verify pertinent updates to GCAT-BCAT-Engine/Publisher
  -> verify pertinent updates to StegVerse-Labs/admissibility-wiki
  -> verify pertinent updates to stegguardian-wiki
```

## Next Actions

1. Observe the current-main Governance validation containing `scripts/validate_external_evidence_interop.py`.
2. Correct only exact failures without removing required checks.
3. Create or extend the StegCore runtime integration task for the five external-evidence cases.
4. Implement the runtime mapper and evaluator without granting the provider execution authority.
5. Publish commit-bound passing evidence only after all original and external cases pass.
6. Apply release-readiness gates only after evidence validity, version uniqueness, ownership, authority boundaries, and downstream declarations pass.
7. Tag or release only after those gates pass.

## Definition of Done

The Governance side of external interoperability is complete when:

- the interface contract is repository-resident;
- all five canonical fixtures are repository-resident;
- CI validates shape, outcomes, stale evidence, drift, incomplete evidence, provider authorization, non-authority, and non-minting;
- continuation requires no original chat or manual-only action.

Full goal activation additionally requires StegCore to evaluate the five fixtures through the actual runtime and publish commit-bound passing evidence.

## Current Completion Assessment

```text
Governance architecture: complete
Original schema and fixtures: complete
Original fixture validator: complete
Ingestion automation: complete
Established StegCore contract integration: complete
Accountability-stack collaboration posture: complete
External evidence-provider interface: complete
External interoperability fixtures: complete
External interoperability repository validator: complete
External interoperability CI wiring: complete
External interoperability StegCore runtime integration: not yet built
External interoperability runtime evidence: not yet published
Established passing evidence record: pending successful StegCore non-PR run
Manual continuation dependency: none
```

## Release Posture

No release or tag is authorized solely by the Governance-side external interoperability build. Release requires successful current-main validation, StegCore runtime integration evidence, version and authority checks, and downstream propagation review.

## Archive Status

This handoff preserves the current decisions, files, fixtures, validation, ownership, authority boundaries, remaining runtime integration, release posture, and permitted continuation scope. Earlier conversation context is not required.
