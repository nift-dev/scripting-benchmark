a := []
i := 1
while(i <= 100000) { a.push(100000 - i + 1); i += 1 }
a = a.sort_by(x => x)
print(a[0])
print(a[100000-1])
print(a[50000-1])
