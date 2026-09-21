from collections import deque
W=200
grid=[[1 if ((r*7+c*13)%5==0 and 0<r<W-1 and 0<c<W-1) else 0 for c in range(W)] for r in range(W)]
q=deque([(0,0)]); dist={(0,0):0}; goal=(W-1,W-1)
while q:
    r,c=q.popleft()
    if (r,c)==goal: break
    for dr,dc in ((1,0),(-1,0),(0,1),(0,-1)):
        nr,nc=r+dr,c+dc
        if 0<=nr<W and 0<=nc<W and grid[nr][nc]==0 and (nr,nc) not in dist:
            dist[(nr,nc)]=dist[(r,c)]+1; q.append((nr,nc))
print(dist[goal])
