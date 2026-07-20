#!/usr/bin/env python3
"""Validate the StegVerse external dependency and replacement registry."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "external_dependency_registry.json"

REQUIRED_TOP_LEVEL = {
    "schema_version",
    "registry_id",
    "status",
    "currency",
    "authority",
    "priority_scale",
    "migration_phases",
    "dependencies",
}

REQUIRED_DEPENDENCY_FIELDS = {
    "id",
    "service_name",
    "category",
    "current_purpose",
    "billing_model",
    "known_monthly_cost",
    "cost_status",
    "billing_cadence",
    "financial_source_evidence",
    "assets_held",
    "lock_in_risk",
    "operational_criticality",
    "sovereignty_impact",
    "priority",
    "replacement_destination",
    "migration_phase",
    "cancellation_blockers",
    "retirement_evidence",
}

REQUIRED_INITIAL_IDS = {
    "render",
    "pypi",
    "github",
    "cloud-space",
    "godaddy",
    "unknown-recurring-services",
}

EXPECTED_PHASES = [
    "DISCOVERED",
    "COST_VERIFICATION",
    "DEPENDENCY_MAPPED",
    "REPLACEMENT_DESIGNED",
    "PARALLEL_OPERATION",
    "MIGRATION_VERIFIED",
    "RETIREMENT_AUTHORIZED",
    "RETIRED",
]

ALLOWED_PRIORITY = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "UNASSESSED"}
ALLOWED_RISK = {"CRITICAL", "HIGH", "MEDIUM", "LOW", "UNASSESSED"}


def fail(message: str) -> None:
    raise ValueError(message)


def require_nonempty_string(value: Any, field: str, dependency_id: str) -> None:
    if not isinstance(value, str) or not value.strip():
        fail(f"{dependency_id}: {field} must be a non-empty string")


def require_string_list(value: Any, field: str, dependency_id: str, *, nonempty: bool) -> None:
    if not isinstance(value, list):
        fail(f"{dependency_id}: {field} must be a list")
    if nonempty and not value:
        fail(f"{dependency_id}: {field} must not be empty")
    if any(not isinstance(item, str) or not item.strip() for item in value):
        fail(f"{dependency_id}: {field} must contain only non-empty strings")


def validate_dependency(item: Any, phases: list[str]) -> str:
    if not isinstance(item, dict):
        fail("each dependency must be an object")

    missing = REQUIRED_DEPENDENCY_FIELDS - item.keys()
    if missing:
        fail(f"dependency missing required fields: {sorted(missing)}")

    dependency_id = item["id"]
    require_nonempty_string(dependency_id, "id", "<unknown>")

    for field in (
        "service_name",
        "category",
        "billing_model",
        "cost_status",
        "billing_cadence",
        "replacement_destination",
        "migration_phase",
    ):
        require_nonempty_string(item[field], field, dependency_id)

    for field in ("current_purpose", "assets_held", "cancellation_blockers"):
        require_string_list(item[field], field, dependency_id, nonempty=True)

    for field in ("financial_source_evidence", "retirement_evidence"):
        require_string_list(item[field], field, dependency_id, nonempty=False)

    cost = item["known_monthly_cost"]
    if cost is not None and (not isinstance(cost, (int, float)) or isinstance(cost, bool) or cost < 0):
        fail(f"{dependency_id}: known_monthly_cost must be null or a non-negative number")

    if cost is None and not item["cost_status"].startswith("UNKNOWN"):
        fail(f"{dependency_id}: null cost must have an UNKNOWN cost_status")

    if item["priority"] not in ALLOWED_PRIORITY:
        fail(f"{dependency_id}: invalid priority {item['priority']}")

    for field in ("lock_in_risk", "operational_criticality", "sovereignty_impact"):
        if item[field] not in ALLOWED_RISK:
            fail(f"{dependency_id}: invalid {field} value {item[field]}")

    if item["migration_phase"] not in phases:
        fail(f"{dependency_id}: invalid migration phase {item['migration_phase']}")

    phase_index = phases.index(item["migration_phase"])
    retirement_index = phases.index("RETIREMENT_AUTHORIZED")
    if phase_index >= retirement_index:
        if not item["retirement_evidence"]:
            fail(f"{dependency_id}: retirement phase requires retirement evidence")
        if item["cancellation_blockers"]:
            fail(f"{dependency_id}: retirement phase cannot retain cancellation blockers")

    return dependency_id


def validate_registry(registry: Any) -> None:
    if not isinstance(registry, dict):
        fail("registry root must be an object")

    missing = REQUIRED_TOP_LEVEL - registry.keys()
    if missing:
        fail(f"registry missing required fields: {sorted(missing)}")

    authority = registry["authority"]
    if not isinstance(authority, dict):
        fail("authority must be an object")

    expected_authority = {
        "registry_grants_cancellation_authority": False,
        "replacement_design_grants_retirement_authority": False,
        "retirement_requires_gdr": True,
    }
    for key, expected in expected_authority.items():
        if authority.get(key) is not expected:
            fail(f"authority boundary violated: {key} must be {expected}")

    phases = registry["migration_phases"]
    if phases != EXPECTED_PHASES:
        fail("migration_phases must preserve the canonical ordered lifecycle")

    priority_scale = registry["priority_scale"]
    if not isinstance(priority_scale, list) or set(priority_scale) != ALLOWED_PRIORITY:
        fail("priority_scale must contain the complete allowed priority set")

    dependencies = registry["dependencies"]
    if not isinstance(dependencies, list) or not dependencies:
        fail("dependencies must be a non-empty list")

    ids = [validate_dependency(item, phases) for item in dependencies]
    if len(ids) != len(set(ids)):
        fail("dependency ids must be unique")

    missing_initial = REQUIRED_INITIAL_IDS - set(ids)
    if missing_initial:
        fail(f"initial confirmed dependencies missing: {sorted(missing_initial)}")


def main() -> int:
    try:
        registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
        validate_registry(registry)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print(f"PASS: validated {len(registry['dependencies'])} external dependencies")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
