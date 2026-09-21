declare -A counts
for ((i=1;i<=1000;i++)); do v=$((i % 10)); counts[$v]=$(( ${counts[$v]:-0} + 1 )); done
echo ${#counts[@]}
echo ${counts[0]}
