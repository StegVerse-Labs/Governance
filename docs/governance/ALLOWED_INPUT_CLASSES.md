# Allowed Input Classes for Governance

Governance evaluates **only structured, bounded inputs**.
Raw data, evidence, or unverified artifacts MUST NOT enter governance.

## Allowed Input Classes

### 1. Verified Continuity Receipts
Source: StegID  
Properties:
- cryptographically verified
- immutable
- revocation-aware

### 2. TRACE Signal Bundles (see TRACE contract)
Source: StegTrace  
Properties:
- confidence-scored
- non-authoritative
- explicitly labeled as inferential

### 3. Policy Configuration
Source: Governance repo
Properties:
- versioned
- auditable
- deterministic

### 4. Execution Context (optional)
Examples:
- request type
- environment tag
- enforcement target

## Explicitly Disallowed Inputs
- Raw documents
- Unverified claims
- Human testimony without verification
- AI-generated conclusions
- Free-text “analysis” blobs

> Governance decides actions, not truth.
