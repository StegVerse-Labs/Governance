#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

HARNESS_PATH = Path("reports/provider-successor-harness-results.json")
MIGRATION_PATH = Path("reports/provider-migration-plans.json")
OUTPUT_PATH = Path("reports/provider-promotion-states.json")


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def load(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path}: expected object")
    return value


def records(document: dict[str, Any], *keys: str) -> list[dict[str, Any]]:
    for key in keys:
        value = document.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def provider_id(item: dict[str, Any]) -> str:
    return str(item.get("provider_id") or item.get("dependency_id") or item.get("id") or "").strip()


def main() -> int:
    harness_doc = load(HARNESS_PATH)
    migration_doc = load(MIGRATION_PATH)
    harness = {provider_id(item): item for item in records(harness_doc, "results", "providers") if provider_id(item)}
    migrations = {provider_id(item): item for item in records(migration_doc, "plans", "providers", "tasks") if provider_id(item)}

    states: list[dict[str, Any]] = []
    for pid in sorted(set(harness) | set(migrations)):
        h = harness.get(pid, {})
        m = migrations.get(pid, {})
        harness_state = str(h.get("state") or "MISSING")
        missing_gates = sorted({str(x) for x in m.get("missing_retirement_gates", m.get("missing_gates", []))})
        blockers = sorted({str(x) for x in h.get("blockers", [])})

        if harness_state == "PASS_NON_PRODUCTION_HARNESS":
            promotion_state = "ELIGIBLE_ISOLATED_IMPLEMENTATION_TEST"
            next_actions = [
                "instantiate_ephemeral_successor_backend",
                "run_fixture_bound_export_import_test",
                "run_fixture_bound_health_test",
                "run_fixture_bound_rollback_test",
                "submit_isolated_test_evidence_to_master_records",
            ]
        else:
            promotion_state = "BLOCKED_NON_PRODUCTION_HARNESS"
            next_actions = [
                "rebuild_prerequisite_chain",
                "reexecute_non_production_harness",
                "persist_machine_readable_blocked_evidence",
            ]
            if not blockers:
                blockers = ["successor_harness_not_passed"]

        state = {
            "provider_id": pid,
            "service_name": m.get("service_name", pid),
            "promotion_state": promotion_state,
            "harness_state": harness_state,
            "harness_result_hash": h.get("result_hash"),
            "missing_retirement_gates": missing_gates,
            "blockers": blockers,
            "next_machine_actions": next_actions,
            "isolated_test_environment_required": True,
            "production_credentials_permitted": False,
            "production_traffic_permitted": False,
            "production_mutation_allowed": False,
            "traffic_cutover_authority": False,
            "execution_authority": False,
            "cancellation_authority": False,
            "provider_retirement_authority": False,
            "continuity_receipt_minted": False,
            "manual_action_required": False,
        }
        state["state_hash"] = digest(state)
        states.append(state)

    report = {
        "schema_version": "1.0.0",
        "promotion_set_id": "metered-platform-provider-promotion-states",
        "source_harness_hash": harness_doc.get("result_set_hash") or harness_doc.get("results_hash"),
        "source_migration_hash": migration_doc.get("plan_set_hash") or migration_doc.get("plans_hash"),
        "states": states,
        "automatic_maximum_state": "ELIGIBLE_ISOLATED_IMPLEMENTATION_TEST",
        "production_credentials_permitted": False,
        "production_traffic_permitted": False,
        "production_mutation_allowed": False,
        "traffic_cutover_authority": False,
        "execution_authority": False,
        "cancellation_authority": False,
        "provider_retirement_authority": False,
        "continuity_receipt_minted": False,
        "manual_action_required": False,
    }
    report["promotion_set_hash"] = digest(report)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(OUTPUT_PATH)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
