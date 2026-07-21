#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REGISTRY = Path("data/external_dependency_registry.json")
OUTPUT = Path("reports/provider-inventory-queue.json")


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    rank = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "UNASSESSED": 4}
    tasks = []
    for dep in registry["dependencies"]:
        missing_assets = dep.get("assets_held", []) in ([], ["unknown"])
        tasks.append({
            "dependency_id": dep["id"],
            "service_name": dep["service_name"],
            "category": dep["category"],
            "priority": dep["priority"],
            "migration_phase": dep["migration_phase"],
            "inventory_state": "BLOCKED_PROVIDER_IDENTIFICATION" if dep["id"] in {"cloud-space", "unknown-recurring-services"} else "READY_FOR_AUTOMATED_DISCOVERY",
            "declared_asset_classes": dep.get("assets_held", []),
            "discovery_actions": [
                "enumerate_accounts_without_exporting_secrets",
                "enumerate_assets_and_configuration_metadata",
                "hash_inventory_snapshot",
                "record_source_commit_and_collection_time",
                "submit_inventory_to_master_records_custody",
            ],
            "blockers": sorted(set(dep.get("cancellation_blockers", []))),
            "asset_classes_unresolved": missing_assets,
            "cancellation_authority": False,
            "provider_retirement_authority": False,
            "traffic_cutover_authority": False,
            "manual_action_required": False,
        })
    tasks.sort(key=lambda item: (rank.get(item["priority"], 9), item["dependency_id"]))
    report = {
        "schema_version": "1.0.0",
        "queue_id": "metered-platform-provider-inventory",
        "source_registry": str(REGISTRY),
        "status": "ACTIVE" if tasks else "EMPTY",
        "selection_rule": "priority_then_dependency_id",
        "tasks": tasks,
        "manual_action_required": False,
        "cancellation_authority": False,
        "provider_retirement_authority": False,
    }
    report["queue_hash"] = hashlib.sha256(canonical(report).encode("utf-8")).hexdigest()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
