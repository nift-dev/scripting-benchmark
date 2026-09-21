a,b=0,1
(2..30).each { a,b=b,a+b }
puts b
