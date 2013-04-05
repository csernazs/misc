

dmax = 0

S2D = {str(x): x for x in xrange(10)}

for a in xrange(100):
    for b in xrange(100):
        res = a**b
        dsum = sum([S2D[x] for x in str(res)])
        if dsum>dmax:
            dmax = dsum
            
            
            
print dmax
