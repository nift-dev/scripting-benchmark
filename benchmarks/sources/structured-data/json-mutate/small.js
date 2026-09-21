const arr=JSON.parse(require('fs').readFileSync('benchmarks/fixtures/structured-data/records-small.json','utf8'));
let total=0;
for(const e of arr){ e.total=e.v*2; total+=e.total; }
console.log(total);
