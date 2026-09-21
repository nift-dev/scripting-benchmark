require 'set'
s=(1..1000).to_set
puts s.size
puts (s.include?(500) ? 1 : 0)
puts (s.include?(1001) ? 1 : 0)
