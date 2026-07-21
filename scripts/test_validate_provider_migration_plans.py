#!/usr/bin/env python3
import json, subprocess, tempfile
from pathlib import Path

V="scripts/validate_provider_migration_plans.py"
H="a"*64
REG={"providers":[{"provider_id":"github","gates":[{"gate":"asset_inventory_complete","verification_state":"EVIDENCE_VERIFIED","evidence_hash":H,"evidence_refs":["x"]}]}]}

def run(plan, ok):
    with tempfile.TemporaryDirectory() as d:
        p=Path(d)/"p.json"; r=Path(d)/"r.json"
        p.write_text(json.dumps(plan)); r.write_text(json.dumps(REG))
        cp=subprocess.run(["python3",V,str(p),str(r)],capture_output=True,text=True)
        assert (cp.returncode==0)==ok, cp.stdout+cp.stderr

run({"providers":[{"provider_id":"github","gate_claims":[{"gate":"asset_inventory_complete","verification_state":"EVIDENCE_VERIFIED","evidence_hash":H}]}]},True)
run({"providers":[{"provider_id":"github","gate_claims":[{"gate":"asset_inventory_complete","verification_state":"EVIDENCE_VERIFIED","evidence_hash":"b"*64}]}]},False)
run({"providers":[{"provider_id":"github","retirement_ready":True,"gate_claims":[]}]},False)
run({"providers":[{"provider_id":"github","execution_authority":True,"gate_claims":[]}]},False)
print("provider migration plan validator tests passed")
