require 'json'
arr=JSON.parse(File.read('benchmarks/fixtures/structured-data/records-small.json'))
puts arr.sum{|e| e['v']}
