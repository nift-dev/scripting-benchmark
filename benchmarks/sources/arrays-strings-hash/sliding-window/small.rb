a=(1..1000).to_a; k=100
cur=a[0,k].sum; best=cur
(k..1000-1).each { |i| cur=cur-a[i-k]+a[i]; best=cur if cur>best }
puts best
