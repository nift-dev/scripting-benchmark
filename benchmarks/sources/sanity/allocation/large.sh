a=()
for ((i=1;i<=100000;i++)); do a+=($i); done
echo ${#a[@]}
