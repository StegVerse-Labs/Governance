#!/usr/bin/env python3
"""
Governance repo validation (no external deps).

Checks:
- Required files exist
- GDR schema is valid JSON and contains required keys
- Core governance docs exist
- README contains a standard privacy banner (tolerant to Unicode variants)
"""
from __future__ import annotations

import json
import re
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

ZERO_WIDTH = [
    "\u200b",  # zero width space
    "\u200c",  # zero width non-joiner
    "\u200d",  # zero width joiner
    "\ufeff",  # BOM / zero width no-break
]

def die(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}")
    sys.exit(code)

def ok(msg: str) -> None:
    print(f"OK: {msg}")

def _normalize(s: str) -> str:
    # Remove invisible chars and emoji variation selectors that break exact matching.
    for ch in ZERO_WIDTH:
        s = s.replace(ch, "")
    s = s.replace("\ufe0f", "")  # variation selector 16
    s = s.replace("\ufe0e", "")  # variation selector 15
    # Normalize common dash variants to a plain hyphen for matching.
    s = s.replace("–", "-").replace("—", "-")
    return s

def _has_privacy_banner(readme_text: str) -> bool:
    t = _normalize(readme_text)

    # Accept any of these signals (keeps it strict but not brittle).
    patterns = [
        r"\*\*Public Repository\*\*",
        r"\*\*Private Repository\*\*",
        r"\*\*Public Repository\s*-\s*TRACE-Processed Content\*\*",
        r"\*\*Public Repository\s*-\s*TRACE\-Processed Content\*\*",
        r"\*\*Public Repository\s*-\s*TRACE Processed Content\*\*",
    ]

    # Also accept the exact quoted banner style (with or without the emoji).
    # Example:
    # > 🔓 **Public Repository**
    # or
    # > **Public Repository**
    quoted_ok = re.search(r"^>\s*(🔓\s*)?\*\*Public Repository\*\*", t, re.MULTILINE) is not None
    quoted_ok |= re.search(r"^>\s*(🔒\s*)?\*\*Private Repository\*\*", t, re.MULTILINE) is not None
    quoted_ok |= re.search(r"^>\s*(📘\s*)?\*\*Public Repository\s*-\s*TRACE-Processed Content\*\*", t, re.MULTILINE) is not None

    if quoted_ok:
        return True

    return any(re.search(p, t) for p in patterns)

def main() -> None:
    missing = [p for p in REQUIRED_FILES if not p.exists()]
    if missing:
        for p in missing:
            print(f"Missing: {p.relative_to(ROOT)}")
        die(f"{len(missing)} required file(s) missing.")

    ok("All required files present.")

    readme_path = ROOT / "README.md"
    readme = readme_path.read_text(encoding="utf-8", errors="replace")
    if not _has_privacy_banner(readme):
        # Helpful debug without leaking content: show the first few lines normalized.
        first_lines = "\n".join(_normalize(readme).splitlines()[:8])
        print("DEBUG (first lines, normalized):")
        print(first_lines)
        die("README is missing a standard privacy classification banner.")
    ok("README contains privacy classification banner.")

    schema_path = ROOT / "schemas" / "gdr.schema.json"
    try:
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
    except Exception as e:
        die(f"Failed to parse schemas/gdr.schema.json as JSON: {e}")

    for key in ["$schema", "$id", "title", "type", "required", "properties"]:
        if key not in schema:
            die(f"gdr.schema.json missing required top-level key: {key}")

    required = set(schema.get("required", []))
    expected = {"gdr_version", "decision_id", "decision", "policy", "evaluated_inputs", "issued_at", "rationale"}
    if not expected.issubset(required):
        die(f"gdr.schema.json required fields do not include expected baseline. Missing: {sorted(expected - required)}")

    ok("gdr.schema.json structure looks sane.")
    print("\nValidation passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()
