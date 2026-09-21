const s=new Set(); for(let i=1;i<=1000;i++) s.add(i);
console.log(s.size)
console.log(s.has(500)?1:0)
console.log(s.has(1001)?1:0)
