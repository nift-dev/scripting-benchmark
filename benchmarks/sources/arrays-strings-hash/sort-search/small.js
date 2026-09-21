const a=Array.from({length:1000},(_,i)=>1000-i).sort((x,y)=>x-y);
console.log(a[0]); console.log(a[1000-1]); console.log(a[500-1]);
