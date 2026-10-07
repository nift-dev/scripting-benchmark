a=($(seq 1000 -1 1))
IFS=$'\n' sorted=($(sort -n <<< "${a[*]}"))
echo ${sorted[0]}
echo ${sorted[1000-1]}
echo ${sorted[500-1]}
