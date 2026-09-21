arr := inject("benchmarks/fixtures/structured-data/records-large.json")
total := 0
for(e : arr) { total += e.v }
print(total)
