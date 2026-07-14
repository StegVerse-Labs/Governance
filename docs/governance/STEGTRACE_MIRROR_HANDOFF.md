# StegTrace Mirror Handoff

**Status:** Active bootstrap handoff  
**Authoritative continuation source:** This file until `StegVerse-Labs/StegTrace` exists and contains its own root `STEGTRACE_MIRROR_HANDOFF.md`.

## Goal

Create `StegVerse-Labs/StegTrace` as the shared TRACE evaluation engine.

StegTrace is not an application-specific implementation and does not own publication data. Application-level access is provided through profiles/adapters such as:

- `StegTalk/trace` — ephemeral communications reconstruction, channel confidence, and local-only signal evaluation
- `StegProv/trace` — persistent research, provenance, authorship, contradiction, and confidence evaluation
- `StegFREEDOM/trace` — oversight, institutional behavior, rights-impact, and accountability evaluation

Domain repositories such as `Genealogy_Hub`, `FREE-DOM_Books`, `FREE-DOM_OverSight`, `StegDJ`, `StegBiography`, `Trumpality`, `Epsteinality`, and `FREE-DOM` hold TRACE-processed data and publication outputs. They are not TRACE engines.

## Required architectural boundaries

- **StegID** verifies continuity and cryptographic claims.
- **StegTrace** evaluates signals, uncertainty, provenance, integrity, corroboration, and confidence.
- **Governance / StegCore** decides what actions are permitted from verified and bounded inputs.
- **StegTalk, StegOps, StegTV, and other downstream systems** enforce valid Governance Decision Records.
- TRACE outputs are non-authoritative and must not be promoted into verified fact without the appropriate StegID evidence and Governance policy.

## Governance dependency already established

Governance defines the consumer-side contracts for:

- TRACE integration
- TRACE Signal Bundles
- GDR enforcement
- StegTalk policy constraints
- confidence labels and non-retroactive decision handling

StegTrace must produce bundles compatible with the Governance copy of `schemas/trace_signal_bundle.schema.json`.

## Required StegTrace bootstrap files

Create the following in `StegVerse-Labs/StegTrace`:

- `README.md`
- `STEGTRACE_MIRROR_HANDOFF.md`
- `CHANGELOG.md`
- `DISCLAIMER.md`
- `CONFIDENCE_LABELS.md`
- `docs/TRACE_OVERVIEW.md`
- `docs/TRACE_SIGNAL_BUNDLE.md`
- `docs/TRACE_PROFILES.md`
- `docs/TRACE_REEVALUATION_AND_DELTAS.md`
- `schemas/trace_signal_bundle.schema.json`
- `scripts/emit_bundle_example.py`
- `scripts/validate_trace.py`
- `.github/workflows/validate-trace.yml`

## Initial implementation requirements

1. Keep the engine public and free of private data, credentials, and raw evidence.
2. Validate the TRACE Signal Bundle schema and a generated example bundle.
3. Preserve immutable artifacts and versioned evaluations in application/data repositories.
4. Treat new evidence as a re-evaluation trigger; never overwrite prior evaluations.
5. Emit explicit confidence deltas explaining upgrades or degradations.
6. Support counter-signals and limitations in every evaluation path.
7. Do not create globally linkable identifiers for StegTalk/TRACE.
8. Keep discovery/search orchestration modular; it may be TRACE-owned without being embedded in the core scoring engine.

## Current blocker

`StegVerse-Labs/StegTrace` was not found through the connected GitHub installation, and the available GitHub mutation tools cannot create a new repository. Repository creation is therefore the only user-owned bootstrap action.

## Ownership

- **User:** create public repository `StegVerse-Labs/StegTrace` with an initialized default branch.
- **Next authorized build session:** read this handoff first, create the required files, open a PR, run validation, and replace this temporary Governance handoff with the root handoff in StegTrace.

## Validation requirements

Before declaring bootstrap complete:

- `validate-trace.yml` must run on pull request, push to `main`, and manual dispatch.
- Required status check must pass.
- Governance and StegTrace schema copies must be byte-equivalent or share an explicit version/hash receipt.
- README must identify StegTrace as the engine and list the application profiles.
- No raw evidence or sensitive data may be committed.

## Permitted continuation scope

The next session may:

- create and populate StegTrace after the repository exists;
- add schemas, docs, validation tooling, examples, and handoff records;
- open a PR and report validation state;
- create integration tasks for StegTalk/trace, StegProv/trace, and StegFREEDOM/trace.

The next session must not:

- treat TRACE confidence as verified truth;
- place raw investigative artifacts in the public engine repo;
- collapse application profiles into separate incompatible TRACE protocols;
- weaken Governance or StegID authority boundaries.

## Completion event

This handoff is superseded when `StegVerse-Labs/StegTrace/STEGTRACE_MIRROR_HANDOFF.md` is committed and verified as the current source of truth.
