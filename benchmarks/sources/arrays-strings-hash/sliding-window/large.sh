a=($(seq 1 100000)); k=10000
cur=0; for ((j=0;j<k;j++)); do cur=$((cur+${a[j]})); done; best=$cur
for ((i=k;i<100000;i++)); do cur=$((cur-${a[$((i-k))]}+${a[$i]})); if ((cur>best)); then best=$cur; fi; done
echo $best
