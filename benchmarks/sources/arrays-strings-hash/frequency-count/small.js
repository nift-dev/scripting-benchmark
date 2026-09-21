const counts = {}
for (let i = 1; i <= 1000; i++) { const v = String(i % 10); counts[v] = (counts[v] || 0) + 1; }
console.log(Object.keys(counts).length)
console.log(counts['0'])
