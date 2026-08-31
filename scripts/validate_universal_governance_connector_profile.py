#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "docs/examples/fixtures/universal_governance_connector_profile.example.json"

REQUIRED_GOV = {"G0","G1","G2","G3","G4","G5","G6"}
REQUIRED_ADM = {"A0","A1","A2","A3","A4","A5","A6","A7","A8"}
DECISIONS = {"ALLOW","DENY","FAIL-CLOSED"}


def load(path: Path):
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("profile root must be object")
    return value


def validate(p: dict) -> None:
    if p.get("schema_version") != "stegverse.governance-connector-profile.v1":
        raise ValueError("schema_version")
    if p.get("runtime", {}).get("evaluator_ref") != "stegcore.three_layer.evaluate_three_layer":
        raise ValueError("evaluator_ref")
    if set(p.get("runtime", {}).get("decision_surface", [])) != DECISIONS:
        raise ValueError("decision_surface")
    if p.get("runtime", {}).get("execution_requires_separate_authority") is not True:
        raise ValueError("execution authority separation")
    system = p.get("system") or {}
    if system.get("enforcement_class") == "ENFORCED" and system.get("bypass_path_declared") is not False:
        raise ValueError("ENFORCED profile cannot declare bypass")
    interlock = p.get("interlock") or {}
    if interlock.get("required") is not True or interlock.get("fail_closed_on_binding_error") is not True:
        raise ValueError("Interlock fail-closed binding")
    if not all(interlock.get(k) for k in ("intr_profile_ref","governed_transition_profile_ref","carrier_profile_ref")):
        raise ValueError("transport/profile refs")
    ops = p.get("operations")
    if not isinstance(ops, list) or not ops:
        raise ValueError("operations")
    seen=set()
    for op in ops:
        oid=op.get("operation_id")
        if not oid or oid in seen:
            raise ValueError("operation ids must be unique")
        seen.add(oid)
        if not set(op.get("required_governance_classes", [])).issubset(REQUIRED_GOV):
            raise ValueError("governance class")
        if not set(op.get("required_admissibility_stages", [])).issubset(REQUIRED_ADM):
            raise ValueError("admissibility stage")
        if op.get("authority_ref_required") is not True or op.get("evidence_refs_required") is not True:
            raise ValueError("authority/evidence requirements")
        if op.get("protected_consequence") is True and op.get("bypass_disposition") != "FAIL_CLOSED":
            raise ValueError("protected consequence must fail closed on bypass")
        if not op.get("policy_ref"):
            raise ValueError("policy_ref")
    evidence=p.get("evidence") or {}
    for key in ("ingress_receipt_required","decision_receipt_required","egress_receipt_required","reconstruction_required"):
        if evidence.get(key) is not True:
            raise ValueError(f"evidence requirement {key}")
    boundaries=p.get("authority_boundaries") or {}
    for key in (
        "profile_grants_execution_authority",
        "interlock_grants_execution_authority",
        "intr_grants_execution_authority",
        "carrier_grants_execution_authority",
        "governance_allow_grants_credential_authority",
    ):
        if boundaries.get(key) is not False:
            raise ValueError(f"authority escalation {key}")
    if boundaries.get("credential_authority") != "TV/TVC":
        raise ValueError("credential authority")


def main() -> int:
    try:
        profile=load(FIXTURE)
        validate(profile)
        # deterministic negative controls
        bad=json.loads(json.dumps(profile))
        bad["system"]["bypass_path_declared"]=True
        try:
            validate(bad)
            raise ValueError("negative control: enforced bypass accepted")
        except ValueError as exc:
            if "bypass" not in str(exc):
                raise
        bad=json.loads(json.dumps(profile))
        bad["authority_boundaries"]["intr_grants_execution_authority"]=True
        try:
            validate(bad)
            raise ValueError("negative control: InTr authority escalation accepted")
        except ValueError as exc:
            if "authority escalation" not in str(exc):
                raise
        bad=json.loads(json.dumps(profile))
        bad["operations"][0]["bypass_disposition"]="OUT_OF_SCOPE_DECLARED"
        try:
            validate(bad)
            raise ValueError("negative control: protected bypass accepted")
        except ValueError as exc:
            if "protected consequence" not in str(exc):
                raise
    except Exception as exc:
        print(f"UNIVERSAL_GOVERNANCE_CONNECTOR_PROFILE: FAIL: {exc}")
        return 1
    print("UNIVERSAL_GOVERNANCE_CONNECTOR_PROFILE: PASS")
    print(f"operations={len(profile['operations'])}")
    print("negative_controls=3")
    print("authority_effect=NONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
