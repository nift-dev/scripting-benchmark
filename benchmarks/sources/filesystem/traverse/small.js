const fs=require('fs'),path=require('path');
function walk(d){ let c=0; for(const e of fs.readdirSync(d,{withFileTypes:true})){ const p=path.join(d,e.name); if(e.isDirectory()) c+=walk(p); else if(p.endsWith('.txt')) c++; } return c; }
console.log(walk('benchmarks/sources/filesystem/traverse/small_tree'));
