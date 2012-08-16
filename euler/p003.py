
from itertools import islice

from math import sqrt, ceil

def primes():
    n = 1
    while True:
        for d in xrange(2, long(ceil(sqrt(n)))):
            if n % d == 0:
                break
        else:
            yield n
        n = n + 2
        

n = 600851475143
n_r = long(sqrt(n))

g = primes()
while True:
    t = g.next()
#    print t
    if t > n_r:
        break
        
    if n % t == 0:
        print "r:", t
    


