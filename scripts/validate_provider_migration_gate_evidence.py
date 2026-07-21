#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

REQUIRED_GATES = [
    "asset_inventory_complete",
    "export_verified",
    "successor_health_verified",
    "parallel_operation_passed",
    "rollback_verified",
    "secrets_rotated",
    "traffic_cutover_verified",
    "master_records_custody_recorded",
]
FORBIDDEN_TRUE = [
    "provider_retirement_authority",
    "cancellation_authority",
    "execution_authority",
    "traffic_cutover_authority",
    "continuity_receipt_minted",
    "manual_action_required",
]
VALID_STATES = {"BLOCKED_MISSING_EVIDENCE", "EVIDENCE_VERIFIED"}


def canonical_hash(value: object) -> str:
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def fail(message: str) -> None:
    raise ValueError(message)


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "data/provider_migration_gate_evidence.json")
    payload = json.loads(path.read_text())

    if payload.get("required_gates") != REQUIRED_GATES:
        fail("required_gates must exactly match the governed retirement gate set")
    for key in FORBIDDEN_TRUE:
        if payload.get(key) is not False:
            fail(f"{key} must be false")

    seen_providers: set[str] = set()
    for provider in payload.get("providers", []):
        provider_id = provider.get("provider_id")
        if not isinstance(provider_id, str) or not provider_id:
            fail("provider_id is required")
        if provider_id in seen_providers:
            fail(f"duplicate provider_id: {provider_id}")
        seen_providers.add(provider_id)

        gates = provider.get("gates")
        if not isinstance(gates, list) or [g.get("gate") for g in gates] != REQUIRED_GATES:
            fail(f"{provider_id}: gates must exactly match required order")
        for gate in gates:
            state = gate.get("verification_state")
            if state not in VALID_STATES:
                fail(f"{provider_id}/{gate.get('gate')}: invalid verification_state")
            evidence_hash = gate.get("evidence_hash")
            evidence_refs = gate.get("evidence_refs")
            if state == "EVIDENCE_VERIFIED":
                if not isinstance(evidence_hash, str) or len(evidence_hash) != 64:
                    fail(f"{provider_id}/{gate.get('gate')}: verified gate requires sha256 evidence_hash")
                if not isinstance(evidence_refs, list) or not evidence_refs:
                    fail(f"{provider_id}/{gate.get('gate')}: verified gate requires evidence_refs")
            else:
                if evidence_hash not in (None, ""):
                    fail(f"{provider_id}/{gate.get('gate')}: blocked gate cannot claim evidence_hash")
            for key in FORBIDDEN_TRUE:
                if gate.get(key, False):
                    fail(f"{provider_id}/{gate.get('gate')}: hidden authority {key}")

        computed = canonical_hash({"provider_id": provider_id, "gates": gates})
        claimed = provider.get("gate_set_hash")
        if claimed is not None and claimed != computed:
            fail(f"{provider_id}: gate_set_hash mismatch")

    print(json.dumps({
        "valid": True,
        "provider_count": len(seen_providers),
        "registry_hash": canonical_hash(payload),
        "provider_retirement_authority": False,
        "cancellation_authority": False,
        "execution_authority": False,
        "traffic_cutover_authority": False,
        "continuity_receipt_minted": False,
        "manual_action_required": False,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"valid": False, "error": str(exc)}), file=sys.stderr)
        raise SystemExit(1)
