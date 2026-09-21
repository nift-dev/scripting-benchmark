a=list(range(1,100000+1)); k=10000
cur=sum(a[:k]); best=cur
for i in range(k,100000):
    cur=cur-a[i-k]+a[i]
    if cur>best: best=cur
print(best)
