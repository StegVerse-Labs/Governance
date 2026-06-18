# Governance Mirror Handoff

## Purpose

This handoff is the source of truth for continuing Governance repository work without requiring prior chat context.

It mirrors the Site handoff pattern for non-Site work: future sessions should read this file before continuing Governance, StegCore policy, resolver, GDR, or constitutional-hardening work.

---

## Current Goal

Harden Governance as the StegVerse constitutional decision layer.

Governance must remain the only place where external reality becomes internal authority. Judicial, regulatory, alliance, emergency, operational, and AI-agent pressure must route through Governance as bounded inputs and produce auditable Governance Decision Records (GDRs) before downstream execution.

---

## Current Status

Completed in this pass:

- Added root-level `CONSTITUTIONAL_ROLE.md`.
- Declared Governance as Layer 1: Core (Constitutional).
- Locked Governance as a decision layer, not an execution layer.
- Explicitly stated that Governance may not verify truth, execute actions, aggregate political authority, or accept raw unverified inputs.
- Added pressure-handling rules requiring external pressure to enter as bounded inputs and produce GDRs.
- Added fail-closed semantics when Governance is unavailable.
- Added AI-agent interaction constraints.

---

## Build Assumptions

- Governance is the canonical policy and GDR layer for StegVerse.
- StegID verifies continuity and truth evidence upstream.
- StegCore interprets, sequences, escalates, or defers Governance outputs downstream.
- StegOps, StegTalk, StegTrace/TRACE, StegTV, StegBrain, and other execution or surface systems must not perform irreversible actions without a valid GDR.
- Governance semantics are additive-only unless a new policy version is explicitly declared.

---

## Immediate Next Work

1. Link `CONSTITUTIONAL_ROLE.md` from `README.md`.
2. Add a constitutional-role validation check to CI.
3. Add or update docs under `docs/governance/` to reference the constitutional layer model.
4. Verify `schemas/gdr.schema.json` contains enough fields to represent pressure-source metadata and authority-scope metadata.
5. Add tests or fixtures for pressure-routed decisions if the repo already has a test structure.

---

## Do Not Do

- Do not make Governance verify receipts or cryptography.
- Do not make Governance execute actions.
- Do not allow raw data, testimony, documents, screenshots, or unverified claims to become direct Governance inputs.
- Do not add emergency bypasses.
- Do not add global political, alliance, or jurisdictional override switches.
- Do not mutate old GDR semantics retroactively.

---

## Done Criteria For This Goal

This goal is complete when:

- `CONSTITUTIONAL_ROLE.md` exists at the repository root.
- README links the constitutional role declaration.
- CI verifies the role declaration exists and contains the required layer phrase.
- Governance docs explicitly state that external pressure routes into GDRs rather than directly into execution.
- GDR schema or examples can represent authority scope and pressure-source metadata.

---

## Current Completion Estimate

- Governance constitutional hardening: 45% complete
- Governance repo activation toward this goal: 45% complete
- Fully developed files vs scaffolding/stubs: 55% complete

The main remaining gap is enforcement: declarations now exist, but CI and schema-level validation still need to make them machine-checkable.

---

## Archive Readiness

This handoff is sufficient for the next session to continue Governance constitutional hardening without reading the full prior chat.
