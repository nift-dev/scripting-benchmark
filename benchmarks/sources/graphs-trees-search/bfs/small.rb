W=20
grid=(0...W).map{|r| (0...W).map{|c| ((r*7+c*13)%5==0 && r>0 && r<W-1 && c>0 && c<W-1) ? 1 : 0 }}
dist=Array.new(W){Array.new(W,-1)}; dist[0][0]=0
q=[[0,0]]; qi=0; goal=W-1
while qi<q.length
  cr,cc=q[qi]; qi+=1
  break if cr==goal && cc==goal
  [[1,0],[-1,0],[0,1],[0,-1]].each do |dr,dc|
    nr=cr+dr; nc=cc+dc
    if nr>=0 && nr<W && nc>=0 && nc<W && grid[nr][nc]==0 && dist[nr][nc]==-1
      dist[nr][nc]=dist[cr][cc]+1; q<<[nr,nc]
    end
  end
end
puts dist[goal][goal]
