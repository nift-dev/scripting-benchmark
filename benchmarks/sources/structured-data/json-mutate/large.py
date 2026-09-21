import json
arr=json.load(open('benchmarks/fixtures/structured-data/records-large.json'))
print(sum(e['total'] if 'total' in e else 0 for e in [{**e,'total':e['v']*2} for e in arr]))
