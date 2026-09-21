a := []
i := 1
while(i <= 100000) { a.push(i); i += 1 }
best := 0
i = 0
while(i < 10000) { best += a[i]; i += 1 }
cur := best
i = 10000
while(i < 100000) { cur = cur - a[i - 10000] + a[i]; if(cur > best) { best = cur }; i += 1 }
print(best)
