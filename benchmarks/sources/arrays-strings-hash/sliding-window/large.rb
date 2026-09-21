a=(1..100000).to_a; k=10000
cur=a[0,k].sum; best=cur
(k..100000-1).each { |i| cur=cur-a[i-k]+a[i]; best=cur if cur>best }
puts best
