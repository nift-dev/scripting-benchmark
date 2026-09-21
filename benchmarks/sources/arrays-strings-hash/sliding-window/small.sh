a=($(seq 1 1000)); k=100
cur=0; for ((j=0;j<k;j++)); do cur=$((cur+${a[j]})); done; best=$cur
for ((i=k;i<1000;i++)); do cur=$((cur-${a[$((i-k))]}+${a[$i]})); if ((cur>best)); then best=$cur; fi; done
echo $best
