counts = {}
for i in range(1, 1000+1):
    v = str(i % 10)
    counts[v] = counts.get(v, 0) + 1
print(len(counts))
print(counts['0'])
