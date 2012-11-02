
from itertools import islice
import c_prime

PRIME_MAX = 1000000
primes = c_prime.get_primes(PRIME_MAX, set)

def quad(a, b):
    n = 0
    while True:
        yield n**2+a*n+b
        n=n+1
        
#print primes
sol_max = 0

for a in xrange(-1000, 1001):
    for b in xrange(-1000, 1001):
        sol = 0
        for idx, n in enumerate(quad(a, b)):
#            print idx, n
            if n > PRIME_MAX:
                raise ValueError(str(n))

            if n<1:
                break
                            
            if n not in primes:
                sol = idx
                break

        if sol>0:        
            print a, b, sol
            if sol>sol_max:
                sol_max = sol
                sol_a, sol_b = a, b
                
print ">"*10
print sol_a, sol_b, sol_max
print sol_a * sol_b

                
    
    