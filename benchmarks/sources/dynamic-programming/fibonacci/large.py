a,b=0,1
for _ in range(2,100001): a,b=b,(a+b)%1000000007
print(b)
