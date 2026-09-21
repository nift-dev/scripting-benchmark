a=()
for ((i=1;i<=1000;i++)); do a+=($i); done
echo ${#a[@]}
