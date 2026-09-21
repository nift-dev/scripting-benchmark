let a=0n,b=1n;
for(let i=2;i<=100000;i++){ const c=(a+b)%1000000007n; a=b; b=c; }
console.log(b.toString());
