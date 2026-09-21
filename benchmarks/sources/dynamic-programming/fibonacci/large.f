a := 0
b := 1
i := 2
while(i <= 100000) { c := (a + b) % 1000000007; a = b; b = c; i += 1 }
print(b)
