
import math
import sys


def calc_n(n):
    if n<10:
        return n
    
    base = 10
    
    idx = 2
    while n>=base:
        oldbase = base
        base = 9*10**(idx-1)*idx + base
        idx = idx + 1

    idx = idx-1
    res = (n-oldbase)/idx+10**(idx-1)
    pos = (n-oldbase) % idx

    return int(str(res)[pos])
    
    

def check():
    extra=0
    data = "".join([str(n) for n in xrange(1000000)])

    for idx, n in enumerate(data):
        n = int(n)
        c = calc_n(idx)
        if n != c: 
            print idx, n, c
            extra += 1
        if extra>20:
            break
        
        

sol = 0

for i in xrange(7):
    n = 10**i
    res = calc_n(n)

    if not sol:
        sol = res
    else:
        sol = sol * res
    print n, res
    
print sol


    