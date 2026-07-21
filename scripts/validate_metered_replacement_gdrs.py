#!/usr/bin/env python3
"""Validate canonical metered-platform replacement Governance Decision Records."""
from __future__ import annotations

import json
import pathlib
import sys

FIXTURES = {
    "docs/examples/fixtures/metered_replacement_selection_gdr.json": {
        "decision": "allow",
        "result": "ALLOW",
        "reason_code": "replacement.selection_allowed",
        "scope": "REPLACEMENT_DESIGN_ONLY",
    },
    "docs/examples/fixtures/metered_replacement_retirement_denied_gdr.json": {
        "decision": "deny",
        "result": "DENY",
        "reason_code": "retirement.evidence_incomplete",
        "scope": "PROVIDER_RETIREMENT",
    },
}

PROHIBITED_TRUE_FIELDS = (
    "provider_retirement_authority",
    "cancellation_authority",
    "continuity_receipt_minted",
)


def load(path: pathlib.Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot load {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def validate_fixture(path_text: str, expected: dict[str, str]) -> list[str]:
    path = pathlib.Path(path_text)
    errors: list[str] = []
    if not path.exists():
        return [f"missing fixture: {path}"]
    try:
        record = load(path)
    except ValueError as exc:
        return [str(exc)]

    if record.get("decision") != expected["decision"]:
        errors.append(f"{path}: unexpected decision")
    if record.get("policy") != {
        "policy_id": "metered-platform-replacement",
        "policy_version": "1.0.0",
    }:
        errors.append(f"{path}: incorrect policy identity")

    execution = record.get("execution_boundary")
    runtime = record.get("runtime_expectation")
    if not isinstance(execution, dict) or not isinstance(runtime, dict):
        return errors + [f"{path}: execution and runtime boundaries are required"]

    if execution.get("result") != expected["result"]:
        errors.append(f"{path}: execution result mismatch")
    if execution.get("scope") != expected["scope"]:
        errors.append(f"{path}: execution scope mismatch")
    if runtime.get("result") != expected["result"]:
        errors.append(f"{path}: runtime result mismatch")
    if runtime.get("reason_code") != expected["reason_code"]:
        errors.append(f"{path}: runtime reason mismatch")

    for field in PROHIBITED_TRUE_FIELDS:
        if execution.get(field) is not False:
            errors.append(f"{path}: execution {field} must be false")
        if runtime.get(field) is not False:
            errors.append(f"{path}: runtime {field} must be false")

    if expected["scope"] == "REPLACEMENT_DESIGN_ONLY":
        boundary = record.get("replacement_boundary", {})
        if boundary.get("retirement_requires_separate_gdr") is not True:
            errors.append(f"{path}: separate retirement GDR must be required")
        prohibited = set(boundary.get("prohibited_actions", []))
        for action in ("cancel_service", "delete_service", "retire_provider"):
            if action not in prohibited:
                errors.append(f"{path}: missing prohibited action {action}")

    if expected["scope"] == "PROVIDER_RETIREMENT":
        boundary = record.get("retirement_boundary", {})
        required = boundary.get("required_evidence", [])
        missing = boundary.get("missing_evidence", [])
        if boundary.get("fail_closed") is not True:
            errors.append(f"{path}: retirement denial must fail closed")
        if not required or set(missing) != set(required):
            errors.append(f"{path}: denial must identify every missing retirement gate")

    return errors


def main() -> int:
    errors: list[str] = []
    for path, expected in FIXTURES.items():
        errors.extend(validate_fixture(path, expected))
    if errors:
        print("Metered replacement GDR validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Metered replacement GDR validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
