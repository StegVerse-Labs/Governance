#!/usr/bin/env python3
import hashlib, json, sys
from pathlib import Path

FORBIDDEN = {"execution_authority","traffic_cutover_authority","cancellation_authority","provider_retirement_authority","continuity_receipt_minted","manual_action_required"}

def canon(v): return json.dumps(v, sort_keys=True, separators=(",",":"), ensure_ascii=False).encode()
def sha(v): return hashlib.sha256(canon(v)).hexdigest()
def truthy_forbidden(v, path="$"):
    out=[]
    if isinstance(v, dict):
        for k,x in v.items():
            if k in FORBIDDEN and bool(x): out.append(f"{path}.{k}")
            out += truthy_forbidden(x, f"{path}.{k}")
    elif isinstance(v, list):
        for i,x in enumerate(v): out += truthy_forbidden(x, f"{path}[{i}]")
    return out

def load(p): return json.loads(Path(p).read_text())

def main():
    plans=load(sys.argv[1] if len(sys.argv)>1 else "reports/provider-migration-plans.json")
    registry=load(sys.argv[2] if len(sys.argv)>2 else "data/provider_migration_gate_evidence.json")
    errors=[]
    gates_by_provider={}
    for pr in registry.get("providers",[]):
        gates_by_provider[pr.get("provider_id")]={g.get("gate"):g for g in pr.get("gates",[])}
    for plan in plans.get("providers", plans.get("plans", [])):
        pid=plan.get("provider_id")
        if not pid or pid not in gates_by_provider:
            errors.append(f"{pid or '<missing>'}: provider absent from gate registry"); continue
        claims=plan.get("gate_claims", plan.get("gates", []))
        for claim in claims:
            gate=claim.get("gate") if isinstance(claim,dict) else claim
            rec=gates_by_provider[pid].get(gate)
            if not rec:
                errors.append(f"{pid}:{gate}: gate absent from registry"); continue
            claimed_state=claim.get("verification_state") if isinstance(claim,dict) else None
            claimed_hash=claim.get("evidence_hash") if isinstance(claim,dict) else None
            if claimed_state=="EVIDENCE_VERIFIED":
                if rec.get("verification_state")!="EVIDENCE_VERIFIED": errors.append(f"{pid}:{gate}: plan claims unverified gate")
                if not claimed_hash or claimed_hash!=rec.get("evidence_hash"): errors.append(f"{pid}:{gate}: evidence hash mismatch")
        if plan.get("eligible_for_retirement") or plan.get("retirement_ready"):
            errors.append(f"{pid}: retirement readiness claim forbidden")
    errors += truthy_forbidden(plans)
    result={"schema_version":"stegverse.governance.provider_migration_plan_validation.v1","valid":not errors,"errors":sorted(set(errors)),"plans_hash":sha(plans),"registry_hash":sha(registry),"manual_action_required":False,"execution_authority":False,"traffic_cutover_authority":False,"cancellation_authority":False,"provider_retirement_authority":False,"continuity_receipt_minted":False}
    print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(0 if result["valid"] else 1)
if __name__=="__main__": main()
