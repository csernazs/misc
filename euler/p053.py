
import scipy.misc

cnt = 0
for n in xrange(1, 101):
    for r in xrange(1, n+1):
        c = scipy.misc.comb(n, r)
        if c>1000000:
            cnt += 1
            
print cnt

        