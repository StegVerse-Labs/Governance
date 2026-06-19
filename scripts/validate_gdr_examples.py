#!/usr/bin/env python3
"""Validate example GDR JSON fixtures against the current schema shape."""
from __future__ import annotations

import json
import pathlib
import sys

REQUIRED_FIELDS = [
    "gdr_version",
    "decision_id",
    "decision",
    "policy",
    "evaluated_inputs",
    "issued_at",
    "rationale",
]

ALLOWED_DECISIONS = {"allow", "deny", "require_review", "recommend"}


def validate_fixture(path: pathlib.Path) -> list[str]:
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"{path}: missing {field}")
    if data.get("gdr_version") != "1.0":
        errors.append(f"{path}: gdr_version must be 1.0")
    if data.get("decision") not in ALLOWED_DECISIONS:
        errors.append(f"{path}: unsupported decision {data.get('decision')}")
    policy = data.get("policy")
    if not isinstance(policy, dict):
        errors.append(f"{path}: policy must be an object")
    else:
        for field in ("policy_id", "policy_version"):
            if field not in policy:
                errors.append(f"{path}: policy missing {field}")
    evaluated_inputs = data.get("evaluated_inputs")
    if not isinstance(evaluated_inputs, dict):
        errors.append(f"{path}: evaluated_inputs must be an object")
    else:
        for field in ("source", "receipt_ids"):
            if field not in evaluated_inputs:
                errors.append(f"{path}: evaluated_inputs missing {field}")
    if not isinstance(data.get("issued_at"), int):
        errors.append(f"{path}: issued_at must be an integer")
    if not isinstance(data.get("rationale"), str):
        errors.append(f"{path}: rationale must be a string")
    return errors


def main() -> int:
    fixture_dir = pathlib.Path("docs/examples/fixtures")
    errors: list[str] = []
    fixtures = sorted(fixture_dir.glob("*.json"))
    if not fixtures:
        print("No GDR fixtures found.")
        return 1
    for fixture in fixtures:
        errors.extend(validate_fixture(fixture))
    if errors:
        print("GDR example fixture validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("GDR example fixture validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
