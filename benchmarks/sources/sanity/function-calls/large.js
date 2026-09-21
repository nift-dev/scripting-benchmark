const inc = x => x + 1
let total = 0
for (let i = 1; i <= 100000; i++) total = inc(total)
console.log(total)
