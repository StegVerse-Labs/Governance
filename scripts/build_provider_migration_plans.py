#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REGISTRY = Path("data/external_dependency_registry.json")
INVENTORY = Path("reports/provider-inventory-results.json")
OUTPUT = Path("reports/provider-migration-plans.json")

REQUIRED_RETIREMENT_GATES = (
    "asset_inventory_complete",
    "export_verified",
    "successor_health_verified",
    "parallel_operation_passed",
    "rollback_verified",
    "secrets_rotated",
    "traffic_cutover_verified",
    "master_records_custody_recorded",
)


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def load_optional(path: Path) -> dict:
    if not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else {}


def collector_state(record: dict) -> str:
    return str(record.get("collector_state") or record.get("status") or record.get("state") or "NOT_COLLECTED")


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    inventory = load_optional(INVENTORY)
    results = {
        str(item.get("provider_id") or item.get("dependency_id")): item
        for item in inventory.get("results", [])
        if isinstance(item, dict)
    }
    plans = []
    for dependency in registry["dependencies"]:
        provider_id = dependency["id"]
        collected = results.get(provider_id, {})
        state = collector_state(collected)
        inventory_complete = state == "COLLECTED" and collected.get("asset_count", 0) > 0
        gates = {gate: False for gate in REQUIRED_RETIREMENT_GATES}
        gates["asset_inventory_complete"] = inventory_complete
        blockers = set(dependency.get("cancellation_blockers", []))
        blockers.update(collected.get("blockers", []))
        plans.append({
            "provider_id": provider_id,
            "service_name": dependency["service_name"],
            "source_inventory_status": state,
            "source_inventory_payload_hash": collected.get("payload_hash"),
            "replacement_destination": dependency.get("replacement_destination"),
            "migration_state": "READY_FOR_SUCCESSOR_DESIGN" if inventory_complete else "BLOCKED_INVENTORY_INCOMPLETE",
            "phases": [
                "inventory_and_dependency_map",
                "successor_design",
                "export_and_reconstruction_test",
                "parallel_operation",
                "rollback_proof",
                "secret_rotation",
                "traffic_cutover_verification",
                "master_records_custody",
                "separate_retirement_gdr",
            ],
            "retirement_gates": gates,
            "missing_retirement_gates": [gate for gate, passed in gates.items() if not passed],
            "blockers": sorted(blockers),
            "manual_action_required": False,
            "execution_authority": False,
            "cancellation_authority": False,
            "provider_retirement_authority": False,
            "traffic_cutover_authority": False,
        })
    plans.sort(key=lambda item: item["provider_id"])
    report = {
        "schema_version": "1.0.1",
        "plan_set_id": "metered-platform-provider-migration-plans",
        "source_registry": str(REGISTRY),
        "source_inventory": str(INVENTORY),
        "plans": plans,
        "manual_action_required": False,
        "execution_authority": False,
        "cancellation_authority": False,
        "provider_retirement_authority": False,
        "traffic_cutover_authority": False,
    }
    report["plan_set_hash"] = hashlib.sha256(canonical(report).encode("utf-8")).hexdigest()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
