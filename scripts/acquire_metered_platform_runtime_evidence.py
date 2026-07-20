#!/usr/bin/env python3
"""Acquire and validate StegCore metered-platform runtime evidence.

This script is intentionally fail-closed but non-interactive. Missing, stale, or
invalid upstream evidence produces a deterministic blocked status instead of a
manual task or an unsupported readiness claim.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

AUTHORITY_FALSE = (
    "provider_retirement_authority",
    "cancellation_authority",
    "continuity_receipt_minted",
)


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def evaluate(source: Path, source_commit: str) -> dict[str, Any]:
    blockers: list[str] = []
    evidence: dict[str, Any] | None = None

    if not source.exists():
        blockers.append("stegcore_runtime_evidence_missing")
    else:
        try:
            loaded = load_json(source)
            if not isinstance(loaded, dict):
                blockers.append("stegcore_runtime_evidence_not_object")
            else:
                evidence = loaded
        except (OSError, json.JSONDecodeError):
            blockers.append("stegcore_runtime_evidence_unreadable")

    if evidence is not None:
        if evidence.get("status") != "pass":
            blockers.append("stegcore_runtime_status_not_pass")
        for field in AUTHORITY_FALSE:
            if evidence.get(field) is not False:
                blockers.append(f"authority_boundary_invalid:{field}")
        cases = evidence.get("cases")
        if not isinstance(cases, list) or not cases:
            blockers.append("runtime_cases_missing")
        else:
            observed = {(case.get("result"), case.get("reason_code")) for case in cases if isinstance(case, dict)}
            required = {
                ("ALLOW", "replacement.selection_allowed"),
                ("DENY", "retirement.evidence_incomplete"),
            }
            if not required.issubset(observed):
                blockers.append("required_runtime_cases_missing")
        recorded_commit = evidence.get("source_commit")
        if source_commit and recorded_commit not in {None, source_commit}:
            blockers.append("source_commit_mismatch")

    payload = {
        "schema_version": "1.0.0",
        "source_repository": "StegVerse-Labs/StegCore",
        "source_commit": source_commit or None,
        "source_path": str(source),
        "status": "pass" if not blockers else "blocked",
        "blockers": sorted(set(blockers)),
        "runtime_evidence_digest": digest(evidence) if evidence is not None else None,
        "provider_retirement_authority": False,
        "cancellation_authority": False,
        "continuity_receipt_minted": False,
    }
    payload["acquisition_digest"] = digest(payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("../stegcore/evidence/metered-platform-runtime.json"))
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--output", type=Path, default=Path("reports/metered-platform-runtime-acquisition.json"))
    args = parser.parse_args()

    result = evaluate(args.source, args.source_commit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"metered platform runtime acquisition: {result['status']}")
    for blocker in result["blockers"]:
        print(f"BLOCKED: {blocker}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
