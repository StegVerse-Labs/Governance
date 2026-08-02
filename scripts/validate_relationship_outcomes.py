#!/usr/bin/env python3
"""Validate canonical relationship/outcome commitments and invariants."""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "docs/examples/relationship-outcome"
SCHEMA = BASE / "relationship_commitment.schema.json"
FIXTURES = {
    "constructive_participation_allow.json": {
        "decision": "ALLOW",
        "relationship_effect": "constructive",
        "outcome_direction": "toward_goal",
    },
    "attention_success_outcome_failure.json": {
        "decision": "REPAIR_REQUIRED",
        "attention_result": "success",
        "relationship_effect": "degrading",
        "outcome_direction": "away_from_goal",
    },
}
REQUIRED = {
    "commitment_version", "commitment_id", "declared_goal", "target_participants",
    "desired_relationship_state", "framing_posture", "participation_cost",
    "expected_constructive_effect", "known_repulsion_risks", "observation_signals",
    "repair_path", "continuation_owner", "completion_evidence", "attention_result",
    "relationship_effect", "outcome_direction", "decision", "authority_boundaries",
}
DECISIONS = {"ALLOW", "ALLOW_WITH_OBSERVATION", "REPAIR_REQUIRED", "DENY"}


def load(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_fixture(path: pathlib.Path, expected: dict[str, str]) -> list[str]:
    errors: list[str] = []
    data = load(path)
    missing = sorted(REQUIRED - data.keys())
    if missing:
        errors.append(f"{path.name}: missing fields: {', '.join(missing)}")
    if data.get("commitment_version") != "1.0.0":
        errors.append(f"{path.name}: commitment_version must be 1.0.0")
    if data.get("decision") not in DECISIONS:
        errors.append(f"{path.name}: unsupported decision")
    if not isinstance(data.get("target_participants"), list) or not data.get("target_participants"):
        errors.append(f"{path.name}: target_participants must be non-empty")
    if not isinstance(data.get("observation_signals"), list) or not data.get("observation_signals"):
        errors.append(f"{path.name}: observation_signals must be non-empty")
    owner = data.get("continuation_owner", "")
    if "/" not in owner or ":" not in owner:
        errors.append(f"{path.name}: continuation_owner must name org/repo:path")
    boundaries = data.get("authority_boundaries", {})
    if boundaries.get("grants_execution_authority") is not False:
        errors.append(f"{path.name}: must not grant execution authority")
    if boundaries.get("mints_continuity_receipt") is not False:
        errors.append(f"{path.name}: must not mint Continuity receipts")
    for field, value in expected.items():
        if data.get(field) != value:
            errors.append(f"{path.name}: expected {field}={value!r}")
    if data.get("attention_result") == "success" and data.get("outcome_direction") == "away_from_goal" and data.get("decision") == "ALLOW":
        errors.append(f"{path.name}: attention success cannot override outcome inversion")
    if data.get("relationship_effect") == "degrading" and data.get("decision") not in {"REPAIR_REQUIRED", "DENY"}:
        errors.append(f"{path.name}: degrading relationship effect must require repair or denial")
    return errors


def main() -> int:
    errors: list[str] = []
    if not SCHEMA.exists():
        errors.append(f"missing schema: {SCHEMA.relative_to(ROOT)}")
    else:
        schema = load(SCHEMA)
        if schema.get("title") != "StegVerse Relationship and Outcome Commitment":
            errors.append("relationship schema title mismatch")
    for filename, expected in FIXTURES.items():
        path = BASE / filename
        if not path.exists():
            errors.append(f"missing fixture: {path.relative_to(ROOT)}")
            continue
        try:
            errors.extend(validate_fixture(path, expected))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"{filename}: {exc}")
    if errors:
        print("Relationship outcome validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Relationship outcome validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
