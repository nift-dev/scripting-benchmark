#!/usr/bin/env python3
import datetime, json, os, platform, shutil, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
runtimes=[('nift',[str(ROOT.parent/'nift/nift'),'--version']),('python',['python3','--version']),('ruby',['ruby','--version']),('lua54',['lua5.4','-v']),('luajit',['luajit','-v']),('node',['node','--version']),('bash',['bash','--version'])]
def ver(cmd):
    if not shutil.which(cmd[0]) and not Path(cmd[0]).exists(): return None
    p=subprocess.run(cmd,text=True,capture_output=True); return ((p.stdout or p.stderr).splitlines() or [''])[0].strip()
out={'schema_version':1,'captured_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'os':{'system':platform.system(),'release':platform.release(),'version':platform.version()},'machine':{'machine':platform.machine(),'processor':platform.processor(),'cpu_count':os.cpu_count()},'runtimes':[{'id':i,'version':ver(c)} for i,c in runtimes]}
(ROOT/'results'/'environment.json').write_text(json.dumps(out,indent=2)+'\n'); print(json.dumps(out,indent=2))
