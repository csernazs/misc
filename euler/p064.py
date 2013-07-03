
import math

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
        
    

cnt = 0
i = 2
while i<=10000:
    seq = list(get(i))
    period = len(seq)-1
    print i, period, seq
    if period % 2:
        cnt += 1
        
    i = i + 1
    while int(math.sqrt(i))**2 == i:
        i = i + 1
    
    
print cnt

    

    