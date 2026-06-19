#!/usr/bin/env python3
"""Validate Governance documentation handoff, required docs, and YAML syntax."""
from __future__ import annotations

import pathlib
import sys

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

REQUIRED_FILES = [
    "README.md",
    "GOVERNANCE_MIRROR_HANDOFF.md",
    "docs/INDEX.md",
    "docs/governance/index.md",
    "docs/governance/constitution.yaml",
    "docs/governance/change_classes.yaml",
    "docs/governance/dual_quorum_protocol.yaml",
    "docs/governance/drift_monitor.yaml",
    "docs/governance/predictive_drift.yaml",
    "docs/governance/anchoring_policy.yaml",
    "docs/governance/internal_credit_policy.yaml",
    "docs/governance/model_lifecycle_review.yaml",
    "docs/governance/did_identity_policy.yaml",
    "docs/governance/ethical_dividend_policy.yaml",
    "docs/governance/adaptive_governance.yaml",
    "docs/governance/plugin_registry_policy.yaml",
    "docs/governance/ai_citizenship_charter.md",
    "docs/policies/risk_register.md",
    ".github/workflows/ingest_bundle.yml",
    ".github/workflows/ingest_conversation.yml",
    ".github/workflows/validate_docs.yml",
]

REQUIRED_HANDOFF_PHRASES = [
    "Source of Truth",
    "Next Actions",
    "Definition of Done",
    "Current Completion Assessment",
]


def validate_required_files() -> list[str]:
    errors: list[str] = []
    for item in REQUIRED_FILES:
        path = pathlib.Path(item)
        if not path.exists():
            errors.append(f"missing required file: {item}")
        elif path.is_file() and not path.read_text(encoding="utf-8").strip():
            errors.append(f"required file is empty: {item}")
    return errors


def validate_yaml() -> list[str]:
    errors: list[str] = []
    for path in sorted(pathlib.Path("docs/governance").glob("*.yaml")):
        try:
            loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid YAML in {path}: {exc}")
            continue
        if loaded is None:
            errors.append(f"YAML file loaded as empty/null: {path}")
    return errors


def validate_handoff() -> list[str]:
    errors: list[str] = []
    path = pathlib.Path("GOVERNANCE_MIRROR_HANDOFF.md")
    if not path.exists():
        return ["handoff file missing"]
    text = path.read_text(encoding="utf-8")
    for phrase in REQUIRED_HANDOFF_PHRASES:
        if phrase not in text:
            errors.append(f"handoff missing phrase: {phrase}")
    return errors


def main() -> int:
    errors = []
    errors.extend(validate_required_files())
    errors.extend(validate_yaml())
    errors.extend(validate_handoff())
    if errors:
        print("Governance documentation validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1
    print("Governance documentation validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
