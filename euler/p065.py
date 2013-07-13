

from fractions import Fraction as F
from itertools import cycle, islice



a=2+F(1,1)

def get_terms():
    a=2
    while True:
        yield 1
        yield a
        yield 1
        a=a+2
    

terms = list(islice(get_terms(), 99))
terms.reverse()

n=terms.pop(0)
x=F(1, n)


while len(terms)>0:
    n = terms.pop(0)
    x = F(1, n + x)

res = 2+x        
print res
print "sol", sum(map(int, str(res.numerator)))
