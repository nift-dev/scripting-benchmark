counts = Hash.new(0)
(1..1000).each { |i| counts[(i % 10).to_s] += 1 }
puts counts.size
puts counts['0']
