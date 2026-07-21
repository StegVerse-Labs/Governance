#!/usr/bin/env python3
"""Execute provider-neutral successor validation without production mutation."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

INDEX = Path("reports/provider-successor-scaffolds.json")
OUTPUT = Path("reports/provider-successor-harness-results.json")


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: expected object")
    return data


def validate_file(path: Path) -> tuple[bool, str | None, dict[str, Any] | None]:
    if not path.exists():
        return False, "artifact_missing", None
    try:
        payload = load_json(path)
    except Exception:
        return False, "artifact_invalid_json", None
    return True, None, payload


def main() -> int:
    index = load_json(INDEX)
    records = index.get("records", index.get("providers", []))
    if not isinstance(records, list):
        raise SystemExit("invalid successor scaffold index")

    results: list[dict[str, Any]] = []
    for record in records:
        if not isinstance(record, dict):
            continue
        provider = str(record.get("provider_id") or record.get("dependency_id") or "").strip()
        if not provider:
            continue
        root = Path("successors") / provider
        required = {
            "interface_contract": root / "interface-contract.json",
            "export_import_map": root / "export-import-map.json",
            "health_checks": root / "health-checks.json",
            "rollback_plan": root / "rollback-plan.json",
            "parallel_fixture": root / "parallel-operation-fixture.json",
        }
        checks: dict[str, Any] = {}
        blockers: list[str] = []
        payloads: dict[str, dict[str, Any]] = {}
        for name, path in required.items():
            ok, blocker, payload = validate_file(path)
            checks[name] = {"passed": ok, "path": str(path)}
            if blocker:
                blockers.append(f"{name}:{blocker}")
            if payload is not None:
                payloads[name] = payload

        production_flags = []
        for payload in payloads.values():
            for key in (
                "production_mutation_allowed",
                "traffic_cutover_authority",
                "cancellation_authority",
                "provider_retirement_authority",
                "execution_authority",
            ):
                if payload.get(key) is True:
                    production_flags.append(key)
        if production_flags:
            blockers.append("forbidden_authority_present")

        scaffold_state = str(record.get("state") or record.get("scaffold_state") or "UNKNOWN")
        executable = not blockers and scaffold_state not in {"BLOCKED_PREREQUISITES", "BLOCKED", "UNKNOWN"}
        state = "PASS_NON_PRODUCTION_HARNESS" if executable else "BLOCKED_PREREQUISITES"
        result = {
            "provider_id": provider,
            "state": state,
            "scaffold_state": scaffold_state,
            "checks": checks,
            "blockers": sorted(set(blockers or ([] if executable else ["successor_prerequisites_incomplete"]))),
            "shadow_execution_only": True,
            "production_mutation_allowed": False,
            "traffic_cutover_authority": False,
            "cancellation_authority": False,
            "provider_retirement_authority": False,
            "execution_authority": False,
            "manual_action_required": False,
        }
        result["result_hash"] = digest(result)
        results.append(result)

    results.sort(key=lambda item: item["provider_id"])
    report = {
        "schema_version": "1.0.0",
        "report_id": "metered-platform-successor-harness-results",
        "source_scaffold_set_hash": index.get("scaffold_set_hash") or index.get("set_hash"),
        "results": results,
        "manual_action_required": False,
        "production_mutation_allowed": False,
        "traffic_cutover_authority": False,
        "cancellation_authority": False,
        "provider_retirement_authority": False,
        "execution_authority": False,
    }
    report["report_hash"] = digest(report)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
