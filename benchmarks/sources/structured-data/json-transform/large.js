const arr=Array.from({length:100000},(_,i)=>({k:i+1,v:(i+1)%7}));
let total=0;
for(const e of arr){ e.total=e.v*2; total+=e.total; }
console.log(total);
