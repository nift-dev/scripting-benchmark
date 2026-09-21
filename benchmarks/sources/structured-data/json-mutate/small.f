arr := inject("benchmarks/fixtures/structured-data/records-small.json")
total := 0
for(e : arr) { e["total"] = e.v * 2; total += e["total"] }
print(total)
