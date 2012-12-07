
from itertools import product
from collections import deque

import prime

primes = prime.get_primes(1000000)
primes = set(primes)


def solve(length):
    print "solve", length
    num = 0
    retval = set()
    for digits in product([1,3,5,7,9], repeat=length):
        digits = deque(digits)
        results = []

        for tmp in xrange(length):
            num = sum([digits[i]*10**(length-i-1) for i in xrange(length)])
            if tmp == 0 and num in retval:
                break
            digits.rotate(1)
            results.append(num)
            if num not in primes:
                break
        else:
            retval.update(results)
            
            

    return sorted(retval)
        
sol = 0
for length in range(2, 7):
    res = solve(length)
    print res
    sol += len(res)
    
print sol+4 # 2,3,5,7
    

