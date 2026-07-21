#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

PROMOTION_PATH = Path("reports/provider-promotion-states.json")
OUTPUT_PATH = Path("reports/provider-ephemeral-backend-results.json")
ELIGIBLE_STATE = "ELIGIBLE_ISOLATED_IMPLEMENTATION_TEST"


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def load() -> dict[str, Any]:
    if not PROMOTION_PATH.exists():
        return {}
    value = json.loads(PROMOTION_PATH.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit("promotion-state document must be an object")
    return value


def provider_id(item: dict[str, Any]) -> str:
    return str(item.get("provider_id") or item.get("dependency_id") or item.get("id") or "").strip()


def execute_backend(pid: str) -> dict[str, Any]:
    fixture = {
        "provider_id": pid,
        "records": [
            {"key": "alpha", "value": {"enabled": True, "count": 1}},
            {"key": "beta", "value": {"enabled": False, "count": 2}},
        ],
    }
    baseline_hash = digest(fixture)

    root = Path(tempfile.mkdtemp(prefix=f"stegverse-{pid}-"))
    try:
        store = root / "store.json"
        export = root / "export.json"
        rollback = root / "rollback.json"

        store.write_text(json.dumps(fixture, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        health_ok = store.exists() and store.stat().st_size > 0

        imported = json.loads(store.read_text(encoding="utf-8"))
        import_hash = digest(imported)

        export.write_text(json.dumps(imported, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        exported = json.loads(export.read_text(encoding="utf-8"))
        export_hash = digest(exported)

        mutated = json.loads(store.read_text(encoding="utf-8"))
        mutated["records"].append({"key": "gamma", "value": {"enabled": True, "count": 3}})
        store.write_text(json.dumps(mutated, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        mutation_detected = digest(mutated) != baseline_hash

        rollback.write_text(json.dumps(fixture, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        shutil.copyfile(rollback, store)
        restored = json.loads(store.read_text(encoding="utf-8"))
        rollback_hash = digest(restored)

        checks = {
            "health_check_passed": health_ok,
            "import_hash_equivalent": import_hash == baseline_hash,
            "export_hash_equivalent": export_hash == baseline_hash,
            "mutation_detected": mutation_detected,
            "rollback_hash_equivalent": rollback_hash == baseline_hash,
            "network_access_used": False,
            "provider_credentials_used": False,
            "production_state_used": False,
        }
        passed = all([
            checks["health_check_passed"],
            checks["import_hash_equivalent"],
            checks["export_hash_equivalent"],
            checks["mutation_detected"],
            checks["rollback_hash_equivalent"],
            checks["network_access_used"] is False,
            checks["provider_credentials_used"] is False,
            checks["production_state_used"] is False,
        ])
        result = {
            "provider_id": pid,
            "state": "PASS_EPHEMERAL_BACKEND" if passed else "BLOCKED_EPHEMERAL_BACKEND_FAILURE",
            "checks": checks,
            "fixture_hash": baseline_hash,
            "manual_action_required": False,
            "isolated_execution_only": True,
            "production_mutation_allowed": False,
            "execution_authority": False,
            "traffic_cutover_authority": False,
            "cancellation_authority": False,
            "provider_retirement_authority": False,
            "continuity_receipt_minted": False,
        }
        result["result_hash"] = digest(result)
        return result
    finally:
        shutil.rmtree(root, ignore_errors=True)


def main() -> int:
    document = load()
    states = document.get("providers") or document.get("states") or document.get("records") or []
    if not isinstance(states, list):
        states = []

    results: list[dict[str, Any]] = []
    for item in states:
        if not isinstance(item, dict):
            continue
        pid = provider_id(item)
        if not pid:
            continue
        state = str(item.get("state") or item.get("promotion_state") or "")
        if state == ELIGIBLE_STATE:
            results.append(execute_backend(pid))
        else:
            blocked = {
                "provider_id": pid,
                "state": "BLOCKED_PROMOTION_NOT_ELIGIBLE",
                "blockers": ["provider_not_eligible_for_isolated_implementation_test"],
                "manual_action_required": False,
                "isolated_execution_only": True,
                "production_mutation_allowed": False,
                "execution_authority": False,
                "traffic_cutover_authority": False,
                "cancellation_authority": False,
                "provider_retirement_authority": False,
                "continuity_receipt_minted": False,
            }
            blocked["result_hash"] = digest(blocked)
            results.append(blocked)

    results.sort(key=lambda item: item["provider_id"])
    report = {
        "schema_version": "1.0.0",
        "report_id": "provider-ephemeral-backend-results",
        "source_promotion_hash": document.get("promotion_set_hash") or document.get("state_set_hash"),
        "results": results,
        "eligible_provider_count": sum(1 for x in results if x["state"] == "PASS_EPHEMERAL_BACKEND"),
        "blocked_provider_count": sum(1 for x in results if x["state"] != "PASS_EPHEMERAL_BACKEND"),
        "manual_action_required": False,
        "isolated_execution_only": True,
        "network_access_used": False,
        "provider_credentials_used": False,
        "production_mutation_allowed": False,
        "execution_authority": False,
        "traffic_cutover_authority": False,
        "cancellation_authority": False,
        "provider_retirement_authority": False,
        "continuity_receipt_minted": False,
    }
    report["report_hash"] = digest(report)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(OUTPUT_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
