#!/usr/bin/env python3
"""Validate canonical governance/admissibility stage-vector fixtures without external dependencies."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURE_DIR = ROOT / "docs" / "examples" / "admissibility"
EXPECTED_STAGES = [f"A{i}" for i in range(9)]
ALLOWED_STATUS = {"PASS", "FAIL", "NOT_RUN", "INDETERMINATE"}
ALLOWED_DISPOSITIONS = {"ALLOW", "DENY", "FAIL_CLOSED", "QUARANTINE", "REPLACEMENT", "FORK", "UNKNOWN"}
REQUIRED_BOUNDARIES = {
    "taxonomy_grants_execution_authority": False,
    "continuity_receipt_minted": False,
    "certification_granted": False,
    "custody_granted": False,
}


def fail(path: Path, message: str) -> None:
    raise ValueError(f"{path.relative_to(ROOT)}: {message}")


def validate(path: Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0.0":
        fail(path, "schema_version must be 1.0.0")
    if not data.get("transition_id"):
        fail(path, "transition_id is required")
    stages = data.get("stages")
    if not isinstance(stages, list) or len(stages) != 9:
        fail(path, "exactly nine stages are required")
    observed = [item.get("stage") for item in stages]
    if observed != EXPECTED_STAGES:
        fail(path, f"stage order must be {EXPECTED_STAGES}, got {observed}")
    for item in stages:
        if item.get("status") not in ALLOWED_STATUS:
            fail(path, f"invalid status at {item.get('stage')}")
        if not isinstance(item.get("evidence_refs"), list):
            fail(path, f"evidence_refs must be a list at {item.get('stage')}")
    disposition = data.get("aggregate_disposition")
    if disposition not in ALLOWED_DISPOSITIONS:
        fail(path, "invalid aggregate_disposition")
    failure_stage = data.get("failure_stage")
    failed = [item["stage"] for item in stages if item["status"] == "FAIL"]
    if disposition == "ALLOW":
        if failed or failure_stage is not None or any(item["status"] != "PASS" for item in stages):
            fail(path, "ALLOW requires every stage PASS and no failure_stage")
    else:
        if failure_stage not in EXPECTED_STAGES:
            fail(path, "non-ALLOW disposition requires a valid failure_stage")
        if failure_stage not in failed:
            fail(path, "failure_stage must identify a stage with FAIL status")
        index = EXPECTED_STAGES.index(failure_stage)
        if any(item["status"] == "PASS" for item in stages[index + 1 :]):
            fail(path, "stages after a failed gate may not PASS")
    boundaries = data.get("authority_boundaries")
    if boundaries != REQUIRED_BOUNDARIES:
        fail(path, f"authority boundaries must equal {REQUIRED_BOUNDARIES}")
    regions = data.get("region_results", [])
    if not isinstance(regions, list):
        fail(path, "region_results must be a list")
    for region in regions:
        if region.get("disposition") not in ALLOWED_DISPOSITIONS:
            fail(path, "invalid regional disposition")
        if not region.get("region_id"):
            fail(path, "region_id is required")


def main() -> int:
    fixtures = sorted(FIXTURE_DIR.glob("*.json"))
    if not fixtures:
        print("No admissibility stage-vector fixtures found", file=sys.stderr)
        return 1
    errors: list[str] = []
    for fixture in fixtures:
        try:
            validate(fixture)
            print(f"PASS {fixture.relative_to(ROOT)}")
        except (ValueError, json.JSONDecodeError) as exc:
            errors.append(str(exc))
            print(f"FAIL {exc}", file=sys.stderr)
    if errors:
        print(f"Validation failed: {len(errors)} fixture(s)", file=sys.stderr)
        return 1
    print(f"Validated {len(fixtures)} admissibility stage-vector fixture(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
