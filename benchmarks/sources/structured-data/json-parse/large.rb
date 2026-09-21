require 'json'
arr=JSON.parse(File.read('benchmarks/fixtures/structured-data/records-large.json'))
puts arr.length
