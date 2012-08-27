
from itertools import islice


def triangle():
    n = 1
    yval = 1
    while True:
        yield yval
        n = n + 1
        yval += n

def get_divisors(n):
    cnt = 2
    for i in xrange(2, n/2+1):
        if n%i == 0:
            cnt += 1

    return cnt

#gen = islice(triangle(), 10)
gen = triangle()
while True:
    i = next(gen)
    divisors = get_divisors(i)
    print i
    
    if divisors>500:
        print i, divisors
        
    
    
        