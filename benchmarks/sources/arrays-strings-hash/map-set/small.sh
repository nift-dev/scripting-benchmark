declare -A s
for ((i=1;i<=1000;i++)); do s[$i]=1; done
echo ${#s[@]}
echo ${s[500]:-0}
echo ${s[1001]:-0}
