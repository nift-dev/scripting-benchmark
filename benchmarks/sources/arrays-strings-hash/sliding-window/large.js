const a=Array.from({length:100000},(_,i)=>i+1); const k=10000;
let cur=0; for(let i=0;i<k;i++) cur+=a[i]; let best=cur;
for(let i=k;i<100000;i++){ cur=cur-a[i-k]+a[i]; if(cur>best) best=cur; }
console.log(best);
