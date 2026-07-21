#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,os,shutil,subprocess,tempfile
from pathlib import Path

OUT=Path('reports/github-complete-history-restoration.json')

def canon(v): return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(v): return hashlib.sha256(canon(v).encode()).hexdigest()
def run(cmd,env=None,cwd=None): return subprocess.run(cmd,check=True,text=True,capture_output=True,env=env,cwd=cwd).stdout.strip()
def refs(path):
    lines=run(['git','-C',str(path),'show-ref']).splitlines()
    return sorted(lines)
def count(path,kind): return int(run(['git','-C',str(path),'rev-list','--all',f'--{kind}-only','--count']))

def main():
    token=os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
    records=[]
    if not token:
        records=[{'repository':'UNRESOLVED','state':'BLOCKED_AUTOMATED_RESTORATION_UNAVAILABLE','blockers':['github_token_unavailable']}]
    else:
        env=dict(os.environ); env['GH_TOKEN']=token
        repos=json.loads(run(['gh','api','installation/repositories','--paginate'],env=env)).get('repositories',[])
        for repo in sorted(repos,key=lambda x:x.get('full_name','')):
            name=repo.get('full_name',''); size=int(repo.get('size') or 0)
            base={'repository':name,'source_private':bool(repo.get('private'))}
            if repo.get('disabled') or size>250000:
                base.update(state='BLOCKED_REPOSITORY_UNSAFE_FOR_RUNNER',blockers=['disabled_or_size_limit'])
                records.append(base); continue
            root=Path(tempfile.mkdtemp(prefix='sv-history-restore-')); src=root/'source.git'; bundle=root/'repo.bundle'; dst=root/'restored.git'
            try:
                url=f"https://x-access-token:{token}@github.com/{name}.git"
                run(['git','clone','--mirror','--quiet',url,str(src)],env=env)
                source_refs=refs(src); source_ref_hash=sha(source_refs)
                commits=count(src,'count'); objects=int(run(['git','-C',str(src),'count-objects','-v']).split('count: ')[1].splitlines()[0])
                run(['git','-C',str(src),'bundle','create',str(bundle),'--all'])
                run(['git','bundle','verify',str(bundle)])
                run(['git','clone','--mirror','--quiet',str(bundle),str(dst)])
                restored_refs=refs(dst); restored_ref_hash=sha(restored_refs)
                restored_commits=count(dst,'count'); restored_objects=int(run(['git','-C',str(dst),'count-objects','-v']).split('count: ')[1].splitlines()[0])
                passed=source_refs==restored_refs and commits==restored_commits and objects==restored_objects
                base.update(state='PASS_ISOLATED_COMPLETE_HISTORY_RESTORATION' if passed else 'BLOCKED_RESTORATION_MISMATCH',source_ref_hash=source_ref_hash,restored_ref_hash=restored_ref_hash,source_commit_count=commits,restored_commit_count=restored_commits,source_loose_object_count=objects,restored_loose_object_count=restored_objects,bundle_sha256=hashlib.sha256(bundle.read_bytes()).hexdigest(),blockers=[] if passed else ['ref_or_object_mismatch'])
            except Exception as exc:
                base.update(state='BLOCKED_AUTOMATED_RESTORATION_FAILURE',blockers=[f'{type(exc).__name__}'])
            finally:
                shutil.rmtree(root,ignore_errors=True)
            base.update(source_retained=False,bundle_retained=False,successor_retained=False,secret_material_included=False,manual_action_required=False,production_mutation_allowed=False,execution_authority=False,traffic_cutover_authority=False,cancellation_authority=False,provider_retirement_authority=False,continuity_receipt_minted=False)
            base['record_hash']=sha(base); records.append(base)
    report={'schema_version':'1.0.0','report_id':'github-complete-history-restoration','records':records,'passed_count':sum(r.get('state')=='PASS_ISOLATED_COMPLETE_HISTORY_RESTORATION' for r in records),'blocked_count':sum(r.get('state')!='PASS_ISOLATED_COMPLETE_HISTORY_RESTORATION' for r in records),'source_retained':False,'bundle_retained':False,'successor_retained':False,'manual_action_required':False,'production_mutation_allowed':False,'execution_authority':False,'traffic_cutover_authority':False,'cancellation_authority':False,'provider_retirement_authority':False,'continuity_receipt_minted':False}
    report['report_hash']=sha(report); OUT.parent.mkdir(parents=True,exist_ok=True); OUT.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
if __name__=='__main__': main()
