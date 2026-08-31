#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
ADAPTER=ROOT/"fixtures/universal-governance-connector/external-adapter.example.json"
REGISTRY=ROOT/"specs/universal-governance-connector-profiles.v1.json"

RANK={"OBSERVABLE":0,"GOVERNED":1,"ENFORCED":2}

def load(p):
    v=json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(v,dict): raise ValueError("object required")
    return v

def resolve(registry,pid):
    for p in registry.get("profiles",[]):
        if p.get("profile_id")==pid: return p
    raise ValueError("adapter governance profile unknown")

def validate(adapter,registry):
    if adapter.get("schema_version")!="stegverse.governance-external-adapter.v1":
        raise ValueError("adapter schema")
    profile=resolve(registry,adapter.get("governance_profile_id"))
    if adapter.get("system_id")!=profile.get("system",{}).get("system_id"):
        raise ValueError("adapter system binding")
    if adapter.get("boundary_id")!=profile.get("system",{}).get("boundary_id"):
        raise ValueError("adapter boundary binding")
    claim=adapter.get("enforcement_claim")
    pclaim=profile.get("system",{}).get("enforcement_class")
    if claim not in RANK or pclaim not in RANK or RANK[claim]>RANK[pclaim]:
        raise ValueError("adapter enforcement claim exceeds profile")
    if claim=="ENFORCED":
        if adapter.get("bypass_path_declared") is not False:
            raise ValueError("ENFORCED adapter cannot declare bypass")
        if not adapter.get("bypass_evidence_refs"):
            raise ValueError("ENFORCED adapter requires bypass evidence")
    ops=adapter.get("operations")
    if not isinstance(ops,list) or not ops: raise ValueError("adapter operations")
    profile_ops={x["operation_id"] for x in profile.get("operations",[])}
    seen=set()
    for op in ops:
        native=op.get("native_operation")
        if not native or native in seen: raise ValueError("native operations unique")
        seen.add(native)
        if op.get("governance_operation_id") not in profile_ops:
            raise ValueError("adapter governance operation unknown")
        if op.get("consequence_authority_ref_required") is not True:
            raise ValueError("separate consequence authority required")
        if not isinstance(op.get("input_mapping"),dict) or not op["input_mapping"]:
            raise ValueError("input mapping")
        if not isinstance(op.get("evidence_mapping"),dict) or not op["evidence_mapping"]:
            raise ValueError("evidence mapping")
    a=adapter.get("authority_boundaries") or {}
    for k in ("adapter_grants_execution_authority","adapter_grants_credential_authority","governance_allow_executes_consequence"):
        if a.get(k) is not False: raise ValueError("adapter authority escalation")
    if a.get("credential_authority")!="TV/TVC": raise ValueError("adapter credential authority")
    if a.get("authority_effect")!="NONE": raise ValueError("adapter authority effect")
    return profile

def main():
    try:
        adapter=load(ADAPTER); registry=load(REGISTRY); validate(adapter,registry)
        bad=json.loads(json.dumps(adapter)); bad["bypass_path_declared"]=True
        try: validate(bad,registry); raise ValueError("negative bypass accepted")
        except ValueError as e:
            if "bypass" not in str(e): raise
        bad=json.loads(json.dumps(adapter)); bad["authority_boundaries"]["adapter_grants_execution_authority"]=True
        try: validate(bad,registry); raise ValueError("negative authority accepted")
        except ValueError as e:
            if "authority escalation" not in str(e): raise
        bad=json.loads(json.dumps(adapter)); bad["operations"][0]["governance_operation_id"]="unknown"
        try: validate(bad,registry); raise ValueError("negative operation accepted")
        except ValueError as e:
            if "operation unknown" not in str(e): raise
    except Exception as e:
        print("UNIVERSAL_GOVERNANCE_EXTERNAL_ADAPTER: FAIL:",e); return 1
    print("UNIVERSAL_GOVERNANCE_EXTERNAL_ADAPTER: PASS")
    print("enforcement_claim=ENFORCED_SOURCE_CONTRACT_ONLY")
    print("negative_controls=3")
    print("authority_effect=NONE")
    return 0
if __name__=="__main__": sys.exit(main())
