import sys
from itertools import *
import c_prime

primes = c_prime.get_primes(10000)
#primes = c_prime.get_primes(10000000)

primes_s = set(primes)

cache = {}
def check(a, b):
#    print a, b
    if (a,b) in cache:
        return cache[(a,b)]
        
    else:
        p1 = int(str(a)+str(b))
        p2 = int(str(b)+str(a))
    
        retval =(p1 in primes_s and p2 in primes_s) or (c_prime.is_prime(p1) and c_prime.is_prime(p2))
        cache[(a,b)] = retval
        return retval
        
        
    

range_max = len(primes)

sol_sum_min = None
sol_min = None

for nidx1 in xrange(range_max):
    print nidx1
    p1 = primes[nidx1]
    for nidx2 in xrange(nidx1+1, range_max):
        p2 = primes[nidx2]
        try:
            c = check(p1, p2)
            if not c:
                continue
        except ValueError:
            break

        if sol_sum_min is not None and p1+p2 > sol_sum_min:
            break
            
        for nidx3 in xrange(nidx2+1, range_max):
            p3 = primes[nidx3]
            try:
                c = check(p1, p3) and check(p2, p3)
                if not c:
                    continue
            except ValueError:
                break

            if sol_sum_min is not None and p1+p2+p3 > sol_sum_min:
                break

            for nidx4 in xrange(nidx3+1, range_max):
                p4 = primes[nidx4]
                try:
                    c = check(p1, p4) and check(p2, p4) and check(p3, p4)
                    if not c:
                        continue
                except ValueError:
                    break

                if sol_sum_min is not None and p1+p2+p3+p4 > sol_sum_min:
                    break


                for nidx5 in xrange(nidx4+1, range_max):
                    p5 = primes[nidx5]
                    try:
                        c = check(p1, p5) and check(p2, p5) and check(p3, p5) and check(p4, p5)
                        if not c:
                            continue
                    except ValueError:
                        break


                    sol = (p1, p2, p3, p4, p5)
#                    print sol
#                    for pair in permutations(sol, 2):
#                        tmp = int("".join(map(str, pair)))
#                        print tmp, c_prime.is_prime(tmp), check(*pair)
                        

                    sol_sum = sum(sol)
                    if sol_sum_min is None or sol_sum < sol_sum_min:
                        sol_sum_min = sol_sum
                        sol_min = sol
                        
                    print "SUM", sol_sum_min, sol_min, sol_sum, sol

print sol_sum_min

