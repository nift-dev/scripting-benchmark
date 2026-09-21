f := file("data.json")
f.open("w")
f.write("[")
i := 1
while(i <= 100000) { if(i > 1) { f.write(",") }; f.write('{"k":' + i.to_string() + ',"v":' + (i % 7).to_string() + '}'); i += 1 }
f.write("]")
f.save()
f.close()
arr := inject("data.json")
total := 0
for(e : arr) { e["total"] = e.v * 2; total += e["total"] }
print(total)
