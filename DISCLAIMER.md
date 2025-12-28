# Disclaimer

This repository defines **governance policy and decision contracts** for StegVerse.

## What this repo provides

- A **policy evaluation model** that operates on **verified inputs**
- A **resolver contract** (Verified Inputs → Governance Decision Record)
- The **GDR** data contract (schema + documentation)

## What this repo does NOT provide

- Cryptographic verification (that is handled by StegID)
- Identity minting or identity proof creation
- Assertions of objective “truth” outside verified inputs

## Not legal or professional advice

Nothing in this repository constitutes legal, financial, medical, or professional advice.

## Safety and ethics

Governance is designed to:
- be auditable and deterministic
- minimize harm from unauthorized capability growth
- enforce deny-by-default egress where required
- keep policy changes reviewable and versioned

For how confidence and uncertainty should be expressed across StegVerse, see `CONFIDENCE_LABELS.md`.
