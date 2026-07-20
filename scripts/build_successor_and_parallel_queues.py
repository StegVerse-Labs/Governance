#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

PLANS_PATH = Path("reports/provider-migration-plans.json")
INVENTORY_PATH = Path("reports/provider-inventory-evidence.json")
SUCCESSOR_OUTPUT = Path("reports/provider-successor-build-queue.json")
PARALLEL_OUTPUT = Path("reports/provider-parallel-operation-plans.json")


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


def list_records(document: dict[str, Any], *keys: str) -> list[dict[str, Any]]:
    for key in keys:
        value = document.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def provider_id(item: dict[str, Any]) -> str:
    return str(item.get("provider_id") or item.get("dependency_id") or item.get("id") or "").strip()


def inventory_state(item: dict[str, Any], plan: dict[str, Any]) -> str:
    return str(
        item.get("collector_state")
        or item.get("status")
        or item.get("state")
        or item.get("inventory_state")
        or plan.get("source_inventory_status")
        or plan.get("inventory_state")
        or "UNKNOWN"
    )


def main() -> int:
    plans_doc = load(PLANS_PATH)
    inventory_doc = load(INVENTORY_PATH)
    plans = list_records(plans_doc, "plans", "providers", "tasks")
    inventory = {
        provider_id(item): item
        for item in list_records(inventory_doc, "providers", "results", "records", "inventory")
        if provider_id(item)
    }

    successor_tasks: list[dict[str, Any]] = []
    parallel_plans: list[dict[str, Any]] = []

    for plan in plans:
        pid = provider_id(plan)
        if not pid:
            continue
        inv = inventory.get(pid, {})
        inv_state = inventory_state(inv, plan)
        destination = str(plan.get("replacement_destination") or plan.get("successor_destination") or "").strip()
        missing_gates = sorted({str(x) for x in plan.get("missing_retirement_gates", plan.get("missing_gates", []))})
        inventory_ready = inv_state in {"COLLECTED", "COMPLETE", "READY", "AVAILABLE"} and int(inv.get("asset_count", 0)) > 0
        destination_ready = bool(destination)
        build_state = "READY_FOR_SUCCESSOR_DESIGN" if inventory_ready and destination_ready else "BLOCKED_PREREQUISITES"
        blockers = []
        if not inventory_ready:
            blockers.append("inventory_not_complete")
        if not destination_ready:
            blockers.append("successor_destination_missing")

        successor_tasks.append({
            "provider_id": pid,
            "service_name": plan.get("service_name", pid),
            "successor_destination": destination,
            "source_inventory_status": inv_state,
            "source_inventory_payload_hash": inv.get("payload_hash") or plan.get("source_inventory_payload_hash"),
            "state": build_state,
            "bounded_actions": [
                "generate_successor_interface_contract",
                "generate_export_import_mapping",
                "generate_health_check_contract",
                "generate_rollback_contract",
                "generate_parallel_operation_fixture",
            ],
            "required_outputs": [
                f"successors/{pid}/interface-contract.json",
                f"successors/{pid}/export-import-map.json",
                f"successors/{pid}/health-checks.json",
                f"successors/{pid}/rollback-plan.json",
                f"successors/{pid}/parallel-operation-fixture.json",
            ],
            "blockers": blockers,
            "manual_action_required": False,
            "execution_authority": False,
            "traffic_cutover_authority": False,
            "cancellation_authority": False,
            "provider_retirement_authority": False,
        })

        parallel_state = "READY_FOR_FIXTURE_GENERATION" if build_state == "READY_FOR_SUCCESSOR_DESIGN" else "BLOCKED_SUCCESSOR_NOT_READY"
        parallel_plans.append({
            "provider_id": pid,
            "state": parallel_state,
            "test_matrix": [
                "read_path_equivalence",
                "write_path_shadowing_without_cutover",
                "artifact_hash_equivalence",
                "health_check_equivalence",
                "failure_injection",
                "rollback_reconstruction",
                "credential_isolation",
                "continuity_record_submission",
            ],
            "success_criteria": {
                "parallel_operation_passed": True,
                "successor_health_verified": True,
                "rollback_verified": True,
                "traffic_cutover_verified": False,
            },
            "missing_retirement_gates": missing_gates,
            "manual_action_required": False,
            "production_mutation_allowed": False,
            "traffic_cutover_authority": False,
            "cancellation_authority": False,
            "provider_retirement_authority": False,
        })

    successor_tasks.sort(key=lambda item: item["provider_id"])
    parallel_plans.sort(key=lambda item: item["provider_id"])

    successor_report = {
        "schema_version": "1.0.1",
        "queue_id": "metered-platform-successor-build",
        "source_plan_hash": plans_doc.get("plan_set_hash") or plans_doc.get("plans_hash"),
        "tasks": successor_tasks,
        "manual_action_required": False,
        "execution_authority": False,
        "traffic_cutover_authority": False,
        "cancellation_authority": False,
        "provider_retirement_authority": False,
    }
    successor_report["queue_hash"] = digest(successor_report)

    parallel_report = {
        "schema_version": "1.0.1",
        "plan_id": "metered-platform-parallel-operation",
        "source_successor_queue_hash": successor_report["queue_hash"],
        "plans": parallel_plans,
        "manual_action_required": False,
        "production_mutation_allowed": False,
        "traffic_cutover_authority": False,
        "cancellation_authority": False,
        "provider_retirement_authority": False,
    }
    parallel_report["plan_hash"] = digest(parallel_report)

    SUCCESSOR_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    SUCCESSOR_OUTPUT.write_text(json.dumps(successor_report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    PARALLEL_OUTPUT.write_text(json.dumps(parallel_report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(SUCCESSOR_OUTPUT)
    print(PARALLEL_OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
