

import c_prime
from itertools import permutations

primes = [x for x in c_prime.get_primes(10000) if x>1000]
primes_set = set(primes)

solved = False
for prime in primes:
#    print prime
    for digits in permutations(map(int, str(prime)), 4):
        if digits[0] == 0 or digits[-1]%2 == 0:
            continue
        num = digits[0]*1000 + digits[1]*100 + digits[2]*10 + digits[3]
        if num == prime:
            continue
        if num<prime:
            continue
             
        if num in primes_set and prime+(num-prime)*2 in primes_set and set(str(prime)) == set(str(prime+(num-prime)*2)):
            print "found", prime, num, prime+(num-prime)*2, num-prime, str(prime)+str(num)+str(prime+(num-prime)*2)
            break
            



    