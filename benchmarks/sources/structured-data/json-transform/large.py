import json
arr=[{"k":i,"v":i%7} for i in range(1,100000+1)]
total=0
for e in arr:
    e['total']=e['v']*2
    total+=e['total']
print(total)
