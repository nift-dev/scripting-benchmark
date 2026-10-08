import sys,json,tempfile,hashlib,time
from pathlib import Path
ROOT=Path('/opt/campaign/scripting-benchmark');sys.path.insert(0,str(ROOT/'scripts'))
from campaign_measure import measure,isolated_env,metadata,identity,summary
from campaign import equivalent
bins={'v4.7.2-source':'/opt/campaign/tools-v472/bin/nift','v4.8.0-source':'/opt/campaign/tools/bin/nift'}
cases=['sanity/noop/small','sanity/loops/large','arrays-strings-hash/frequency-count/large','arrays-strings-hash/sort-index/large','structured-data/json-transform/large']
d=dict(purpose='Same-node diagnostic of substantial changes; never pooled with official results',samples=5,warmups=2,machine=metadata(ROOT),tools={k:identity(v,['--version']) for k,v in bins.items()},source_revisions={'v4.7.2-source':'becae31dba39e5250478ae8d76acc8fe71573ce6','v4.8.0-source':'c80c2cd6f4a2e782e861431637af014bb8a0668c'},compiler_policy='Both built from source with the same compiler and native make defaults on this node',started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),proc_stat_before=Path('/proc/stat').read_text(),jobs=[],publishable=False)
for case in cases:
 family,size=case.rsplit('/',1);cat,bench=family.split('/');src=ROOT/f'benchmarks/sources/{family}/{size}.n';gold=ROOT/f'benchmarks/golden/{cat}__{bench}__{size}.txt'
 # Resolve the manifest extension rather than assume one.
 manifest=json.loads((ROOT/'benchmarks/manifest.json').read_text());ext=next(l['extension'] for l in manifest['languages'] if l['id']=='nift');src=src.with_suffix('.'+ext)
 for version,exe in bins.items():d['jobs'].append(dict(id=case+'/'+version,command=[exe,str(src)],golden=str(gold),source_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),oracle_sha256=hashlib.sha256(gold.read_bytes()).hexdigest(),samples=[]))
output=Path('/opt/campaign/evidence/same-node-version-diagnostic.json')
with tempfile.TemporaryDirectory(prefix='diagnostic-home-') as td:
 env=isolated_env(td)
 for r in range(7):
  jobs=d['jobs'][r%len(d['jobs']):]+d['jobs'][:r%len(d['jobs'])]
  for j in jobs:
   rec,out,err=measure(j['command'],ROOT,env,180)
   rec.update(correct=rec['exit_code']==0 and not rec['timeout'] and equivalent(out,Path(j['golden']).read_bytes()),warmup=r<2,round=r)
   j['samples'].append(rec);output.write_text(json.dumps(d,indent=2)+'\n')
   if not rec['correct']:raise SystemExit('diagnostic correctness failure: '+j['id'])
  print('diagnostic round',r+1,flush=True)
for j in d['jobs']:j['summary']=summary([r for r in j['samples'] if not r['warmup']])
d['publishable']=True;d['ended_utc']=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime());d['proc_stat_after']=Path('/proc/stat').read_text();output.write_text(json.dumps(d,indent=2)+'\n')
