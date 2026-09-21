require 'json'
arr=JSON.parse(File.read('benchmarks/fixtures/structured-data/records-large.json'))
total=0
arr.each{|e| e['total']=e['v']*2; total+=e['total']}
puts total
