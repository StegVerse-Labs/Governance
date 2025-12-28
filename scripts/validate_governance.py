#!/usr/bin/env python3
"""
Governance repo validation (no external deps).

Checks:
- Required files exist
- README contains privacy banner
- GDR schema is valid JSON and contains required keys
- TRACE Signal Bundle schema is valid JSON and contains required keys
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
    # Schemas
    ROOT / "schemas" / "gdr.schema.json",
    ROOT / "schemas" / "trace_signal_bundle.schema.json",
    # Core governance docs
    ROOT / "docs" / "governance" / "GOVERNANCE_DECISION_RECORD.md",
    ROOT / "docs" / "governance" / "POLICY_EVALUATION_MODEL.md",
    ROOT / "docs" / "governance" / "RESOLVER_CONTRACT.md",
    ROOT / "docs" / "governance" / "ROLE_OF_GOVERNANCE.md",
    ROOT / "docs" / "governance" / "TRACE_INTEGRATION.md",
    ROOT / "docs" / "governance" / "TRACE_SIGNAL_BUNDLE.md",
    ROOT / "docs" / "governance" / "STEGTALK_POLICY_PROFILE.md",
    ROOT / "docs" / "governance" / "GDR_ENFORCEMENT_PROFILE.md",
]

def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}")
    sys.exit(code)

def ok(msg: str) -> None:
    print(f"OK: {msg}")

def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        die(f"Failed to parse {path.relative_to(ROOT)} as JSON: {e}")
    raise AssertionError("unreachable")

def require_keys(obj: dict, keys: list[str], name: str) -> None:
    for k in keys:
        if k not in obj:
            die(f"{name} missing required top-level key: {k}")

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
    banner_markers = [
        "🔓 **Public Repository**",
        "🔒 **Private Repository**",
        "📘 **Public Repository – TRACE-Processed Content**",
    ]
    if not any(m in readme for m in banner_markers):
        die("README is missing a standard privacy classification banner.")
    ok("README contains privacy classification banner.")

    # ---- Schema checks: GDR ----
    gdr_path = ROOT / "schemas" / "gdr.schema.json"
    gdr = load_json(gdr_path)
    require_keys(gdr, ["$schema", "$id", "title", "type", "required", "properties"], "gdr.schema.json")

    required = set(gdr.get("required", []))
    expected = {"gdr_version", "decision_id", "decision", "policy", "evaluated_inputs", "issued_at", "rationale"}
    if not expected.issubset(required):
        die(f"gdr.schema.json required fields missing: {sorted(expected - required)}")
    ok("gdr.schema.json structure looks sane.")

    # ---- Schema checks: TRACE Signal Bundle ----
    tsb_path = ROOT / "schemas" / "trace_signal_bundle.schema.json"
    tsb = load_json(tsb_path)
    require_keys(tsb, ["$schema", "$id", "title", "type", "required", "properties"], "trace_signal_bundle.schema.json")

    tsb_required = set(tsb.get("required", []))
    tsb_expected = {"bundle_version", "bundle_id", "produced_at", "subject", "signals"}
    if not tsb_expected.issubset(tsb_required):
        die(f"trace_signal_bundle.schema.json required fields missing: {sorted(tsb_expected - tsb_required)}")
    ok("trace_signal_bundle.schema.json structure looks sane.")

    print("\nValidation passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
