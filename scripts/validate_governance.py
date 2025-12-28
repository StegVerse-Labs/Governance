#!/usr/bin/env python3
"""
Governance repo validation (no external deps).

Checks:
- Required files exist
- GDR schema is valid JSON and contains required keys
- Core governance docs exist
- README contains privacy banner
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    ROOT / "README.md",
    ROOT / "DISCLAIMER.md",
    ROOT / "CONFIDENCE_LABELS.md",
    ROOT / "schemas" / "gdr.schema.json",
    ROOT / "docs" / "governance" / "GOVERNANCE_DECISION_RECORD.md",
    ROOT / "docs" / "governance" / "POLICY_EVALUATION_MODEL.md",
    ROOT / "docs" / "governance" / "RESOLVER_CONTRACT.md",
    ROOT / "docs" / "governance" / "ROLE_OF_GOVERNANCE.md",
    ROOT / "docs" / "governance" / "TRACE_INTEGRATION.md",
    ROOT / "docs" / "governance" / "STEGTALK_POLICY_PROFILE.md",
]

def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}")
    sys.exit(code)

def ok(msg: str) -> None:
    print(f"OK: {msg}")

def main() -> None:
    # Existence checks
    missing = [p for p in REQUIRED_FILES if not p.exists()]
    if missing:
        for p in missing:
            print(f"Missing: {p.relative_to(ROOT)}")
        die(f"{len(missing)} required file(s) missing.")

    ok("All required files present.")

    # README banner check
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    banner_markers = ["ð **Public Repository**", "ð **Private Repository**", "ð **Public Repository â TRACE-Processed Content**"]
    if not any(m in readme for m in banner_markers):
        die("README is missing a standard privacy classification banner.")
    ok("README contains privacy classification banner.")

    # Schema checks
    schema_path = ROOT / "schemas" / "gdr.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as e:
        die(f"Failed to parse schemas/gdr.schema.json as JSON: {e}")

    for key in ["$schema", "$id", "title", "type", "required", "properties"]:
        if key not in schema:
            die(f"gdr.schema.json missing required top-level key: {key}")

    # Ensure required fields listed match baseline contract
    required = set(schema.get("required", []))
    expected = {"gdr_version", "decision_id", "decision", "policy", "evaluated_inputs", "issued_at", "rationale"}
    if not expected.issubset(required):
        die(f"gdr.schema.json required fields do not include expected baseline. Missing: {sorted(expected - required)}")

    ok("gdr.schema.json structure looks sane.")

    print("\nValidation passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
