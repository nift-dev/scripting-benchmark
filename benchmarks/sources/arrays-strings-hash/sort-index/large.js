const a=Array.from({length:100000},(_,i)=>100000-i).sort((x,y)=>x-y);
console.log(a[0]); console.log(a[100000-1]); console.log(a[50000-1]);
