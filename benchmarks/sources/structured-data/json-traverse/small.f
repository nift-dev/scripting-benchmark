arr := inject("benchmarks/fixtures/structured-data/records-small.json")
total := 0
for(e : arr) { total += e.v }
print(total)
