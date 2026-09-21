require 'json'
arr=(1..1000).map{|i| {'k'=>i,'v'=>i%7} }
total=0
arr.each{|e| e['total']=e['v']*2; total+=e['total'] }
puts total
