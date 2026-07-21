#!/usr/bin/env python3
"""Build a deterministic, fail-closed status record for metered-platform replacement."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

REGISTRY = Path("data/external_dependency_registry.json")
COSTS = Path("data/external_cost_evidence.json")
OUTPUT = Path("reports/metered-platform-replacement-status.json")

REQUIRED_RETIREMENT_GATES = {
    "asset_inventory_complete",
    "export_verified",
    "successor_health_verified",
    "parallel_operation_passed",
    "rollback_verified",
    "secrets_rotated",
    "traffic_cutover_verified",
    "master_records_custody_recorded",
}


def canonical_hash(value: object) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def main() -> int:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    costs = json.loads(COSTS.read_text(encoding="utf-8"))
    evidence = costs.get("evidence", [])
    verified_ids = {
        row.get("dependency_id") for row in evidence if row.get("verification_status") == "VERIFIED"
    }

    dependencies = []
    for dep in registry["dependencies"]:
        retirement = set(dep.get("retirement_evidence", []))
        missing = sorted(REQUIRED_RETIREMENT_GATES - retirement)
        dependencies.append({
            "dependency_id": dep["id"],
            "migration_phase": dep["migration_phase"],
            "cost_verified": dep["id"] in verified_ids,
            "retirement_ready": not missing and dep["migration_phase"] == "MIGRATION_VERIFIED",
            "missing_retirement_gates": missing,
            "manual_action_required": False,
        })

    status = {
        "schema_version": "1.0.0",
        "state": "ACTIVE_DISCOVERY",
        "dependencies": dependencies,
        "verified_cost_count": len(verified_ids),
        "retirement_ready_count": sum(1 for d in dependencies if d["retirement_ready"]),
        "manual_repository_tasks": [],
        "authority": {
            "cancellation_authorized": False,
            "provider_retirement_authorized": False,
            "continuity_receipt_minted": False,
        },
    }
    status["status_hash"] = canonical_hash(status)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(status, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT} ({status['status_hash']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
