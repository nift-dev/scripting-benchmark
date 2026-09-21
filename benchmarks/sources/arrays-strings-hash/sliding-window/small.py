a=list(range(1,1000+1)); k=100
cur=sum(a[:k]); best=cur
for i in range(k,1000):
    cur=cur-a[i-k]+a[i]
    if cur>best: best=cur
print(best)
