# Governance Mirror Handoff

## Repository

- Organization: StegVerse-Labs
- Repository: Governance
- Current goal: establish a durable, iPhone-friendly governance documentation hub for StegCore / StegVerse.
- Current activation target: enable repo-managed capture of governance design, conversation continuity, and codified policies without requiring local CLI access.

## Source of Truth

This file is the current handoff and task source of truth for Governance work.

For this repo, continue from this file before adding or modifying governance docs, workflows, indexes, or automation.

## Current Build State

The Governance repo is intended to hold:

1. StegCore constitutional governance specs.
2. Dual-species human/AI governance and economic protocols.
3. Drift detection, anchoring, identity, microledger, vault bridge, and marketplace policies.
4. Conversation capture workflows for preserving working context.
5. Bundle ingestion workflows for iPhone-only creation and refresh of multiple docs.

## Immediate Goal

Create the minimum working documentation automation layer:

- `github/workflows/ingest_bundle.yml` creates/updates docs from a single marked bundle file.
- `github/workflows/ingest_conversation.yml` splits pasted conversations into indexed topic notes.
- `docs/bundles/stegverse_bundle.md` stores the governance bundle source.
- `docs/INDEX.md` becomes the navigation entry point after bundle ingestion.

Note: Workflow file paths live under `.github/...`; when documented for the user, display them without the leading dot and note that the leading dot was intentionally omitted for readability.

## Governance Topics Captured So Far

- Constitutional dual-species governance.
- Human/AI quorum requirements.
- Auto-quorum limits for safety and continuity only.
- Change classes A/B/C/D.
- Predictive drift and early warning.
- Agent-to-agent internal microledger.
- ModelOps lifecycle governance.
- Ledger-anchored DID policy.
- Ethical dividend and reinvestment.
- Adaptive governance parameters.
- Plugin marketplace policy.
- Risk register.
- Draft governance license.
- 30-day pilot plan.

## Next Actions

1. Confirm the bundle ingestion workflow exists and can parse `docs/bundles/stegverse_bundle.md`.
2. Confirm the conversation ingestion workflow exists and can create `docs/conversations/INDEX.md`.
3. Run the bundle ingestion workflow once to generate docs.
4. Review generated docs for malformed YAML caused by copied mathematical symbols or action strings.
5. Add or update `docs/governance/index.md` if a separate governance-only index is desired.
6. After docs are generated, decide whether to add FastAPI stubs in a code repo or keep Governance as documentation-only.

## Definition of Done

The current handoff is complete when:

- A maintainer can open this file and know the next action without reading the full chat.
- The repo contains workflows to ingest a whole conversation or a marked governance bundle.
- The bundle can generate the governance docs and indexes from one source file.
- A future session can continue from this file without needing prior chat context.

## Current Completion Assessment

- Fully developed files: handoff and workflow scaffolds once present.
- Scaffolding/stubs: governance policy YAML and Markdown drafts are intentionally draft-level until wired to implementation.
- Activation requires one successful bundle ingestion run and review of generated docs.

## Archive Status

Once the bundle and ingestion workflows are present, this chat thread can be archived for Governance repo continuity; the repo handoff contains enough context to continue.