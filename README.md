🔓 **Public Repository**

This repository contains protocol specifications, engines, or methodology.  It contains **no private data**, **no credentials**, and **no sensitive artifacts**.

# Governance (StegCore Policy + Resolver)

## What this repo is

**Governance** is StegVerse’s policy layer: it takes **verified inputs** (typically from **StegID**) and produces an auditable, portable decision record called a **GDR (Governance Decision Record)**.

Governance answers:

> “Given verified facts, what actions are permitted, under what constraints, and with what required review?”

Governance does **not** verify cryptography and does **not** decide “truth.”  
It is downstream of verification (StegID) and upstream of enforcement (StegOps, StegTalk, StegTrace/TRACE, StegTV, etc.).

## Key guarantees

- **Deterministic** for given inputs + policy version + configuration
- **Auditable** outputs (GDR) with rationale and evaluated input references
- **Versioned** policies and contracts
- **Safe for humans and AI** consumers

## Repository layout

- `.github/workflows/`
  - `forward-to-bridge.yml` — forwards PRs to the Hybrid Collab Bridge for AI review
  - `validate-governance.yml` — validates schemas + required governance docs
- `app/`
  - `resolver.py` — minimal “policy resolver” component (Verified Inputs → GDR)
- `data/`
  - `stegtvc_config.json` — StegTVC model/provider resolver config
- `docs/governance/`
  - `ROLE_OF_GOVERNANCE.md` — what governance is and is not
  - `POLICY_EVALUATION_MODEL.md` — how evaluation works and what inputs are allowed
  - `RESOLVER_CONTRACT.md` — resolver rules and output requirements
  - `GOVERNANCE_DECISION_RECORD.md` — GDR contract (human-readable)
  - `TRACE_INTEGRATION.md` — how StegCore consumes TRACE outputs safely
  - `STEGTALK_POLICY_PROFILE.md` — StegTalk tier policy rules expressed for governance
- `schemas/`
  - `gdr.schema.json` — JSON Schema for a Governance Decision Record
- `scripts/`
  - `validate_governance.py` — CI validation script (no external deps)
- `stegtvc_client.py`
  - convenience import for GitHub Actions and other automations

## Using the resolver

The repo currently includes a minimal StegTVC resolver used by workflows/agents.

### Quick test (local)
```bash
python app/resolver.py
```

### Import in a workflow or tool
```python
from stegtvc_client import resolve

cfg = resolve(use_case="connectivity-check", module="hybrid-collab-bridge")
print(cfg)
```

## How decisions are produced (conceptual)

1. **StegID verifies** receipts (signatures, continuity, revocation, etc.)
2. Governance **evaluates verified inputs** using a **policy** and emits a **GDR**
3. Downstream systems enforce:
   - allow / deny / require_review / recommend
   - plus any machine hints and constraints

## Governance is intentionally separate from truth

- **StegID** answers: “What happened, and can it be proven?”
- **Governance** answers: “Given verified facts, what should happen next?”
- **TRACE (StegTrace)** answers: “What do we believe about signals/artifacts, with what confidence, and why?”

## Documents for legal/ethical clarity

- `DISCLAIMER.md`
- `CONFIDENCE_LABELS.md`

## Contributing

- All changes via PR
- `main` is protected
- Schemas and core docs must pass CI validation
