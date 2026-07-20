#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

QUEUE = Path("reports/provider-successor-build-queue.json")
PARALLEL = Path("reports/provider-parallel-operation-plans.json")
ROOT = Path("successors")
INDEX = Path("reports/provider-successor-scaffolds.json")


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def digest(value: object) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"{path}: expected object")
    return value


def main() -> int:
    queue = load(QUEUE)
    parallel = load(PARALLEL)
    plans = {
        str(item.get("provider_id")): item
        for item in parallel.get("plans", [])
        if isinstance(item, dict) and item.get("provider_id")
    }
    records: list[dict[str, Any]] = []

    for task in queue.get("tasks", []):
        if not isinstance(task, dict):
            continue
        provider = str(task.get("provider_id", "")).strip()
        if not provider:
            continue
        state = str(task.get("state", "BLOCKED_PREREQUISITES"))
        destination = str(task.get("successor_destination", ""))
        blocked = state != "READY_FOR_SUCCESSOR_DESIGN"
        base = ROOT / provider
        authority = {
            "execution_authority": False,
            "production_mutation_allowed": False,
            "traffic_cutover_authority": False,
            "cancellation_authority": False,
            "provider_retirement_authority": False,
            "continuity_receipt_minted": False,
        }
        common = {
            "schema_version": "1.0.0",
            "provider_id": provider,
            "successor_destination": destination,
            "state": "BLOCKED_PREREQUISITES" if blocked else "SCAFFOLDED_NOT_IMPLEMENTED",
            "blockers": sorted({str(x) for x in task.get("blockers", [])}),
            "manual_action_required": False,
            **authority,
        }
        interface = {
            **common,
            "contract": "provider-successor-interface@1.0",
            "operations": ["inventory", "export", "import", "health", "rollback", "verify"],
            "secret_material_permitted": False,
        }
        export_map = {
            **common,
            "contract": "provider-export-import-map@1.0",
            "mappings": [],
            "unmapped_assets_fail_closed": True,
        }
        health = {
            **common,
            "contract": "provider-successor-health@1.0",
            "checks": ["availability", "integrity", "read_equivalence", "write_shadow_equivalence"],
            "all_checks_required": True,
        }
        rollback = {
            **common,
            "contract": "provider-successor-rollback@1.0",
            "steps": ["freeze_candidate_state", "verify_source_unchanged", "restore_previous_route", "verify_recovery"],
            "automatic_cutover_allowed": False,
        }
        fixture = {
            **common,
            "contract": "provider-parallel-operation-fixture@1.0",
            "test_matrix": plans.get(provider, {}).get("test_matrix", []),
            "production_traffic_percent": 0,
            "shadow_writes_only": True,
        }
        documents = {
            "interface-contract.json": interface,
            "export-import-map.json": export_map,
            "health-checks.json": health,
            "rollback-plan.json": rollback,
            "parallel-operation-fixture.json": fixture,
        }
        hashes: dict[str, str] = {}
        for name, document in documents.items():
            write_json(base / name, document)
            hashes[name] = digest(document)
        record = {
            "provider_id": provider,
            "state": common["state"],
            "files": sorted(hashes),
            "file_hashes": hashes,
            "manual_action_required": False,
            **authority,
        }
        record["record_hash"] = digest(record)
        records.append(record)

    records.sort(key=lambda item: item["provider_id"])
    report = {
        "schema_version": "1.0.0",
        "scaffold_set_id": "metered-platform-successor-scaffolds",
        "source_queue_hash": queue.get("queue_hash"),
        "records": records,
        "manual_action_required": False,
        "execution_authority": False,
        "production_mutation_allowed": False,
        "traffic_cutover_authority": False,
        "cancellation_authority": False,
        "provider_retirement_authority": False,
        "continuity_receipt_minted": False,
    }
    report["scaffold_set_hash"] = digest(report)
    write_json(INDEX, report)
    print(INDEX)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
