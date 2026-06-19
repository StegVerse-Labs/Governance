# Governance Validation Guide

This guide explains how to validate the repository without relying on chat history.

## Primary validation path

Use GitHub Actions:

1. Open the repository Actions tab.
2. Run `Validate Governance Docs`.
3. Confirm the workflow reports: `Governance documentation validation passed.`

Workflow path is displayed here without the leading dot for readability. Actual path:

- `github/workflows/validate_docs.yml`

## What validation checks

The validator confirms:

- required handoff files exist;
- required governance docs exist;
- required indexes exist;
- governance YAML files parse successfully;
- the handoff includes source-of-truth, next action, definition-of-done, and completion sections.

## Local validation path

If local execution is available:

```bash
python -m pip install pyyaml
python scripts/validate_docs.py
```

## If validation fails

1. Read the first error line.
2. Fix missing files before YAML syntax.
3. If YAML fails, check indentation first.
4. Update `GOVERNANCE_MIRROR_HANDOFF.md` after any material change.

## Definition of passing

The repo is validation-ready when both of these are true:

- `Validate Governance Docs` passes in GitHub Actions.
- `GOVERNANCE_MIRROR_HANDOFF.md` contains enough next-step context to continue without the originating chat thread.
