#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

GATES = [
    "asset_inventory_complete",
    "export_verified",
    "successor_health_verified",
    "parallel_operation_passed",
    "rollback_verified",
    "secrets_rotated",
    "traffic_cutover_verified",
    "master_records_custody_recorded",
]

SOURCES = {
    "asset_inventory_complete": Path("reports/provider-inventory-results.json"),
    "export_verified": Path("reports/github-provider-export-snapshot.json"),
    "successor_health_verified": Path("reports/provider-ephemeral-backend-results.json"),
    "parallel_operation_passed": Path("reports/provider-successor-parallel-queues.json"),
    "rollback_verified": Path("reports/provider-ephemeral-backend-results.json"),
    "secrets_rotated": Path("reports/provider-secrets-rotation-evidence.json"),
    "traffic_cutover_verified": Path("reports/provider-traffic-cutover-evidence.json"),
    "master_records_custody_recorded": Path("reports/master-records-provider-custody-evidence.json"),
}


def digest(value: object) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def read(path: Path) -> object | None:
    try:
        return json.loads(path.read_text())
    except Exception:
        return None


def provider_ids() -> list[str]:
    registry = read(Path("data/external_dependency_registry.json")) or {}
    values = registry.get("dependencies", registry.get("providers", [])) if isinstance(registry, dict) else []
    found = []
    for item in values if isinstance(values, list) else []:
        pid = item.get("provider_id") or item.get("id")
        if isinstance(pid, str) and pid:
            found.append(pid)
    return sorted(set(found))


def evidence_for(provider_id: str, gate: str) -> dict:
    path = SOURCES[gate]
    payload = read(path)
    verified = False
    if isinstance(payload, dict):
        records = payload.get("providers") or payload.get("results") or payload.get("repositories") or []
        for record in records if isinstance(records, list) else []:
            rid = record.get("provider_id") or record.get("id")
            if gate in {"export_verified", "parallel_operation_passed"} and provider_id == "github":
                rid = rid or "github"
            state = str(record.get("state") or record.get("status") or record.get("collector_state") or "")
            if rid == provider_id and (state.startswith("PASS") or state.startswith("COLLECTED") or state.startswith("ELIGIBLE")):
                verified = True
                break
    return {
        "gate": gate,
        "verification_state": "EVIDENCE_VERIFIED" if verified else "BLOCKED_MISSING_EVIDENCE",
        "evidence_hash": digest(payload) if verified else None,
        "evidence_refs": [str(path)] if verified else [],
        "manual_action_required": False,
        "provider_retirement_authority": False,
        "cancellation_authority": False,
        "execution_authority": False,
        "traffic_cutover_authority": False,
        "continuity_receipt_minted": False,
    }


def main() -> None:
    providers = []
    for provider_id in provider_ids():
        gates = [evidence_for(provider_id, gate) for gate in GATES]
        providers.append({
            "provider_id": provider_id,
            "gates": gates,
            "gate_set_hash": digest({"provider_id": provider_id, "gates": gates}),
            "all_gates_verified": all(g["verification_state"] == "EVIDENCE_VERIFIED" for g in gates),
            "provider_retirement_authority": False,
            "cancellation_authority": False,
            "execution_authority": False,
            "traffic_cutover_authority": False,
            "continuity_receipt_minted": False,
            "manual_action_required": False,
        })
    payload = {
        "schema_version": "1.0.0",
        "registry_type": "provider_migration_gate_evidence",
        "required_gates": GATES,
        "providers": providers,
        "manual_action_required": False,
        "provider_retirement_authority": False,
        "cancellation_authority": False,
        "execution_authority": False,
        "traffic_cutover_authority": False,
        "continuity_receipt_minted": False,
    }
    Path("data/provider_migration_gate_evidence.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"provider_count": len(providers), "registry_hash": digest(payload)}, sort_keys=True))


if __name__ == "__main__":
    main()
