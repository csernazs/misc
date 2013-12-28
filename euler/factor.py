
import sys
import time
from prime import get_primes


def set_max(max):
    global MAX, primes, primes_set
    MAX = max
    t1 = time.time()
    primes = get_primes(MAX)
    print time.time()-t1

    primes_set = set(primes)

set_max(10000000)

print "max", primes[-1]

cache = {}    
def prime_factor(n):
    assert n<=MAX
    if n in primes_set:
        return [n]
    n_orig = n
    
    n_2 = n/2
    low = 0
    high = len(primes)-1

    while True:
        mid = low + (high-low)/2
#        print "HLM", high, low, mid
        if high-low <= 1:
            break


        if n_2<primes[mid]:
            high = mid
        elif n_2>primes[mid]:
            low = mid
        else:
            break

#    print "===", n, high, mid, low, primes[high], primes[high-1], primes[low]
    
#    return
        
    retval = []
    for i in reversed(primes[:high]):
#       if n in primes_set:
#            retval.append(n)
#            break
        while n % i == 0:
            n = n / i
            if n!=1 and n in cache:
                print "cache", n, cache[n]
                retval.append(i)
                retval.extend(cache[n])
                return retval
            else:
                retval.append(i)
#            if i == 2:
#                return retval
                
        if n==1:
            break
    cache[n_orig] = retval
    return retval

factor = prime_factor    

if __name__ == "__main__":
#    factor(18181)
#    print factor(199991)
#    print prime_factor(199982)
    for i in xrange(2, 1000000):
       res = prime_factor(i)
       print i, res
        