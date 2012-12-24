
import c_prime
primes = c_prime.get_primes(100000)
primes_set = set(primes)
import math

for n in xrange(9, primes[-1]+4, 2):
    if n not in primes_set:
        for base in xrange(1, int(math.sqrt(n/2))+1):
            if (n - (2*base**2)) in primes_set:
                break
        else:
            print n
            break
            
                            
    
