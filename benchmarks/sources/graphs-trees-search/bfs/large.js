const W=200;
const grid=Array.from({length:W},(_,r)=>Array.from({length:W},(_,c)=>((r*7+c*13)%5===0&&r>0&&r<W-1&&c>0&&c<W-1)?1:0));
const dist=Array.from({length:W},()=>Array(W).fill(-1)); dist[0][0]=0;
const q=[[0,0]]; let qi=0; const goal=W-1;
while(qi<q.length){
  const [cr,cc]=q[qi++];
  if(cr===goal&&cc===goal) break;
  for(const [dr,dc] of [[1,0],[-1,0],[0,1],[0,-1]]){
    const nr=cr+dr,nc=cc+dc;
    if(nr>=0&&nr<W&&nc>=0&&nc<W&&grid[nr][nc]===0&&dist[nr][nc]===-1){ dist[nr][nc]=dist[cr][cc]+1; q.push([nr,nc]); }
  }
}
console.log(dist[goal][goal]);
