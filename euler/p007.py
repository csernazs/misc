
from math import ceil
from itertools import islice

def isprime(n):
    for i in xrange(2, int((n**0.5)+1)):
        if n % i == 0:
            return False
    
    return True

def primegen():
    yield 2
    n = 3
    while True:
        if isprime(n):
            yield n
        n += 2

for idx, i in enumerate(islice(primegen(), 10001)):
    print "%d\t%d" % (idx+1, i)
    
    
    
        
    
            
    