s := set()
i := 1
while(i <= 100000) { s.add(i); i += 1 }
print(s.size())
if(s.contains(50000)) { print(1) } else { print(0) }
if(s.contains(100001)) { print(1) } else { print(0) }
