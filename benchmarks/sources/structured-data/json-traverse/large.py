import json
arr=json.load(open('benchmarks/fixtures/structured-data/records-large.json'))
print(sum(e['v'] for e in arr))
