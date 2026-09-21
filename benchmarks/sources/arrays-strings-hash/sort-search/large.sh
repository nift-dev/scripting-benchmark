a=($(seq 100000 -1 1))
IFS=$'\n' sorted=($(sort -n <<< "${a[*]}"))
echo ${sorted[0]}
echo ${sorted[100000-1]}
echo ${sorted[50000-1]}
