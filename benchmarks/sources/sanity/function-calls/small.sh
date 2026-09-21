inc() { total=$(( total + 1 )); }
total=0
for ((i=1;i<=1000;i++)); do inc; done
echo $total
