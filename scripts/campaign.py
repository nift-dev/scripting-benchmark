#!/usr/bin/env python3
"""Run explicit complete workload families; never merge historical campaigns."""
import argparse, hashlib, json, shutil, tempfile
from pathlib import Path
from decimal import Decimal, InvalidOperation
from campaign_measure import measure, isolated_env, metadata, identity, summary
ROOT=Path(__file__).resolve().parents[1]


def equivalent(a,b):
    if a.strip()==b.strip(): return True
    try:
        x,y=Decimal(a.strip().decode()),Decimal(b.strip().decode())
        return x.is_finite() and y.is_finite() and x==y
    except (InvalidOperation,UnicodeDecodeError): return False


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--families',required=True,help='comma-separated category/benchmark families')
    ap.add_argument('--samples',type=int,default=10)
    ap.add_argument('--warmups',type=int,default=2)
    ap.add_argument('--timeout',type=int,default=120)
    ap.add_argument('--nift',required=True)
    ap.add_argument('--output',required=True)
    a=ap.parse_args()
    if a.samples<5: ap.error('at least five samples required')
    manifest=json.loads((ROOT/'benchmarks/manifest.json').read_text())
    families=a.families.split(','); jobs=[]; tools={}
    for lang in manifest['languages']:
        cmd=lang['command'].copy()
        if lang['id']=='nift': cmd=[cmd[0],'{source}']
        cmd[0]=str(Path(a.nift).resolve()) if lang['id']=='nift' else shutil.which(cmd[0])
        if not cmd[0]: raise SystemExit('missing runtime '+lang['id'])
        tools[lang['id']]=identity(cmd[0],['-v'] if lang['id'] in ('lua54','luajit') else ['--version'])
        for family in families:
            cat,bench=family.split('/')
            if cat in lang.get('excluded_categories',[]): continue
            if not any(c['id']==cat and bench in c['benchmarks'] for c in manifest['categories']):
                raise SystemExit('unknown workload '+family)
            for size in manifest['sizes']:
                src=ROOT/'benchmarks/sources'/cat/bench/(size+'.'+lang['extension'])
                gold=ROOT/'benchmarks/golden'/f'{cat}__{bench}__{size}.txt'
                if not src.exists() or not gold.exists(): raise SystemExit('incomplete family: '+str(src))
                jobs.append(dict(id=f'{family}/{size}/{lang["id"]}',
                                 command=[c.replace('{source}',str(src)) for c in cmd],
                                 golden=gold, source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),
                                 oracle_sha256=hashlib.sha256(gold.read_bytes()).hexdigest(),
                                 workload_version=manifest.get('benchmark_versions',{}).get(bench,1), samples=[]))
    result=dict(schema=3,machine=metadata(ROOT),tools=tools,families=families,
                mode='fresh-process-repeated',warmups=a.warmups,samples=a.samples,jobs=[],publishable=False)
    dest=Path(a.output); dest.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='scripting-home-') as td:
        env=isolated_env(td)
        for round_no in range(a.warmups+a.samples):
            order=jobs[round_no%len(jobs):]+jobs[:round_no%len(jobs)]
            for job in order:
                rec,out,err=measure(job['command'],ROOT,env,a.timeout)
                rec['correct']=rec['exit_code']==0 and not rec['timeout'] and equivalent(out,job['golden'].read_bytes())
                rec['warmup']=round_no<a.warmups; rec['round']=round_no
                job['samples'].append(rec)
                result['jobs']=[{k:v for k,v in j.items() if k!='golden'} for j in jobs]
                dest.write_text(json.dumps(result,indent=2)+'\n')
                if not rec['correct']:
                    raise SystemExit('correctness failed: '+job['id']+'; retained non-publishable evidence')
            print(f'round {round_no+1}/{a.warmups+a.samples}',flush=True)
    for j in result['jobs']: j['summary']=summary([r for r in j['samples'] if not r['warmup']])
    result['publishable']=True
    dest.write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__': main()
