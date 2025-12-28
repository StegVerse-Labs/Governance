# Changelog

All notable changes to the **StegVerse Governance** repository will be documented in this file.

This project follows a **contract-first** philosophy:
- Core contracts are versioned and frozen once released
- Additive changes are allowed without breaking compatibility
- Breaking changes require an explicit version bump

---

## [v0.1.0] — 2025-01-__

### Summary
Initial stable release of **Governance v0**, establishing the policy and decision layer for StegVerse.  
This release freezes all core governance contracts and defines the automation boundary for downstream systems.

---

### Added

#### Core Contracts
- **Governance Decision Record (GDR)** contract
- **GDR Enforcement Profile** defining governance-first automation boundaries
- **TRACE Signal Bundle** contract (bounded, confidence-scored, non-authoritative)
- **Resolver Contract** (Verified Inputs → GDR)
- **Policy Evaluation Model**
- **Role of Governance** documentation (explicit separation from truth and verification)

#### Schemas
- `schemas/gdr.schema.json`
- `schemas/trace_signal_bundle.schema.json`

#### Tooling & Automation
- Deterministic governance resolver (`resolver.py`)
- CI validation script (`validate_governance.py`)
- GitHub Actions workflow:
  - runs on pull requests
  - runs on push to `main`
  - supports manual `workflow_dispatch`

#### Documentation
- Governance README with explicit scope and guarantees
- Legal & ethical clarity documents:
  - `DISCLAIMER.md`
  - `CONFIDENCE_LABELS.md`

---

### Guarantees Introduced
- Deterministic decision outputs for given inputs and policy versions
- Non-retroactive Governance Decision Records
- Deny-by-default enforcement for irreversible actions
- Bounded inputs only:
  - Verified Continuity Receipts (StegID)
  - TRACE Signal Bundles
- Safe for both human and AI consumers

---

### Explicit Non-Goals
Governance does **not**:
- Verify cryptographic truth (StegID responsibility)
- Determine factual correctness or provenance (TRACE responsibility)
- Execute actions (StegOps / StegTalk / StegTV responsibility)

---

### Stability & Versioning
- **Governance v0 API surface is frozen**
- Allowed without version bump:
  - New policy documents
  - New schema versions alongside existing ones
- Breaking changes require **v0.2.0+**

---

### Compatibility
- Compatible with:
  - StegID Continuity Receipts
  - TRACE Signal Bundle v1.0
  - Hybrid Collab Bridge review workflows

---

## [Unreleased]

### Planned
- Additional governance policy documents
- Downstream enforcement adapters (StegTalk, StegOps)
- Governance metrics and observability hooks (non-authoritative)

---

_End of changelog_
