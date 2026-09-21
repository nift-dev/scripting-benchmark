declare -A s
for ((i=1;i<=100000;i++)); do s[$i]=1; done
echo ${#s[@]}
echo ${s[50000]:-0}
echo ${s[100001]:-0}
