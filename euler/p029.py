

res = set()
for a in xrange(2, 101):
    for b in xrange(2, 101):
        res.add(a**b)
        
print len(res)
