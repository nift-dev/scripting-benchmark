arr := []
i := 1
while(i <= 100000) { arr.push(i % 10); i += 1 }
g := arr.group_by(x => x)
print(g.size())
print(g["0"].size())
