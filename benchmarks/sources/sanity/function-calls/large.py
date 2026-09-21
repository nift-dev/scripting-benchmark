def inc(x): return x + 1
total = 0
for i in range(1, 100000+1): total = inc(total)
print(total)
