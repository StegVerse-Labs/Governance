# Implementation Placement Decision Note

## Purpose

This note separates governance documentation from executable implementation work so future sessions can continue without relying on chat context.

## Current Assumption

The Governance repo is the source of truth for policy, resolver contracts, decision records, validation, and handoff continuity.

Executable service endpoints should usually live in a code repo unless they are directly part of the existing Governance resolver.

## Recommended Placement

| Work item | Recommended location | Reason |
| --- | --- | --- |
| Policy docs | Governance | This repo is the policy and resolver source of truth. |
| YAML governance drafts | Governance | They define review requirements and boundaries. |
| GDR schema updates | Governance | Existing schemas already live here. |
| Conversation capture workflows | Governance | These preserve documentation continuity. |
| Runtime API endpoints | StegCore or SCW | Runtime endpoints belong with deployable services. |
| Vault / treasury implementation | Token Vault / finance repo | Requires separate legal, treasury, and security review. |
| Site publishing | Site | Public display and mirror work belongs in Site. |

## Default Rule

If a change defines policy, put it in Governance.
If a change executes runtime behavior, put it in the relevant code repo.
If a change publishes documentation externally, put it in Site.

## Next Candidate Integration Goal

After the Governance docs validation passes, the next integration candidate is:

1. map governance drafts to resolver schema fields;
2. produce sample Governance Decision Records for dual-quorum and drift-review cases;
3. decide whether those examples live under `examples/` or `docs/examples/`.
