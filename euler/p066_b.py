
from fractions import Fraction as F
from itertools import cycle

def get(S):

    m = 0
    d = 1
    a0 = 1
    while a0**2<S:
        a0 += 1

    a0 -= 1
    yield a0

    a = a0
    while True:
        m = d*a - m
        d = (S-m**2)/d
        a = (a0+m)/d
        yield a    
        if a == 2*a0:
            break

seq = list(get(2))

s = seq.pop(0)

n = None

seq_c = cycle(seq)

for i in xrange(100):
    if n is None:
        d = seq_c.next()
        n = F(1, d)
    else:
        n = F(1, n.denominator+F(1, seq_c.next()))
    
    print s+n, float(s+n)
    
    

print seq