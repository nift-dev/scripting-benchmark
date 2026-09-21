inc() { total=$(( total + 1 )); }
total=0
for ((i=1;i<=100000;i++)); do inc; done
echo $total
