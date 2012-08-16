

# simple and stupid

res = 0

for i in xrange(1000):
    if i%3 == 0 or i%5 == 0:
        res += i

print res
    
