t=0
for ((i=1;i<=100000;i++)); do t=$((t + i*i)); done
echo $t
