const s=new Set(); for(let i=1;i<=100000;i++) s.add(i);
console.log(s.size)
console.log(s.has(50000)?1:0)
console.log(s.has(100001)?1:0)
