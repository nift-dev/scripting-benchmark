const arr=JSON.parse(require('fs').readFileSync('benchmarks/fixtures/structured-data/records-small.json','utf8'));
console.log(arr.reduce((a,e)=>a+e.v,0));
