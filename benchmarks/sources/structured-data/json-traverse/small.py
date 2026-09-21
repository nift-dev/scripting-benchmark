import json
arr=json.load(open('benchmarks/fixtures/structured-data/records-small.json'))
print(sum(e['v'] for e in arr))
