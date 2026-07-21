#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path

SCHEMA='stegverse.governance.render_successor_spec.v1'
FORBIDDEN={'envVars','env','secretFiles','deployHook','apiKey','token','password','secret'}

def canon(v): return json.dumps(v,sort_keys=True,separators=(',',':')).encode()
def sha(v): return hashlib.sha256(canon(v)).hexdigest()

def clean(v):
    if isinstance(v,dict):
        return {k:clean(x) for k,x in sorted(v.items()) if k not in FORBIDDEN}
    if isinstance(v,list): return [clean(x) for x in v]
    return v

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--source',default='evidence/render-provider-state.json'); ap.add_argument('--output',default='evidence/render-successor-spec.json'); a=ap.parse_args()
    p=Path(a.source)
    blockers=[]; services=[]; configs=[]; source_hash=None
    if not p.exists():
        blockers.append('render_provider_state_missing')
    else:
        try:
            src=json.loads(p.read_text()); source_hash=src.get('report_sha256') or sha(src)
            for s in src.get('services',[]):
                s=clean(s); st=str(s.get('type') or s.get('service_type') or 'unknown').lower()
                cls={'web_service':'container_service','web':'container_service','worker':'worker_service','cron_job':'scheduled_job','cron':'scheduled_job','redis':'managed_cache','key_value':'managed_cache','postgres':'managed_database','private_service':'internal_service','static_site':'static_site'}.get(st,'unsupported_service')
                rec={'source_service_id':s.get('id'),'name':s.get('name'),'source_type':st,'successor_class':cls,'region':s.get('region'),'plan':s.get('plan'),'runtime':s.get('runtime'),'repo':s.get('repo'),'branch':s.get('branch'),'build_command_present':bool(s.get('buildCommand') or s.get('build_command')),'start_command_present':bool(s.get('startCommand') or s.get('start_command')),'environment_value_count':None,'environment_values_retained':False}
                rec['spec_sha256']=sha(rec); services.append(rec)
                if cls=='unsupported_service': blockers.append(f"unsupported_service:{rec.get('name') or rec.get('source_service_id') or 'unknown'}")
            for c in src.get('repository_configurations',[]):
                rec={'repository':c.get('repository'),'path':c.get('path'),'content_sha256':c.get('content_sha256'),'parsed':c.get('parsed',False)}; rec['spec_sha256']=sha(rec); configs.append(rec)
            if not src.get('authenticated_access',False): blockers.append('authenticated_render_metadata_unavailable')
        except Exception as e: blockers.append('invalid_render_provider_state:'+type(e).__name__)
    services=sorted(services,key=lambda x:(str(x.get('name')),str(x.get('source_service_id')))); configs=sorted(configs,key=lambda x:(str(x.get('repository')),str(x.get('path')))); blockers=sorted(set(blockers))
    state='SUCCESSOR_SPEC_READY' if services and not blockers else 'BLOCKED_SUCCESSOR_SPEC'
    out={'schema':SCHEMA,'provider_id':'render','state':state,'source_report_sha256':source_hash,'services':services,'repository_configurations':configs,'service_count':len(services),'configuration_count':len(configs),'blockers':blockers,'manual_action_required':False,'credentials_required_from_user':False,'environment_values_retained':False,'production_mutation_allowed':False,'execution_authority':False,'traffic_cutover_authority':False,'cancellation_authority':False,'provider_retirement_authority':False,'continuity_receipt_minted':False}
    out['spec_sha256']=sha(out); Path(a.output).parent.mkdir(parents=True,exist_ok=True); Path(a.output).write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
if __name__=='__main__': main()
