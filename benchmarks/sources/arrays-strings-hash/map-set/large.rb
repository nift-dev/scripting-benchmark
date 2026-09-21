require 'set'
s=(1..100000).to_set
puts s.size
puts (s.include?(50000) ? 1 : 0)
puts (s.include?(100001) ? 1 : 0)
