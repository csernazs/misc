
import c_prime
from itertools import product

primes = [x for x in c_prime.get_primes(1000000)]
primes_set = set(map(str, primes))

digits_s = map(str, range(10))

solved = False

# very brute force
# plenty of spaces for improvements

for prime in primes:
    prime_s = str(prime)
    for src in sorted(set(prime_s)):
        if prime_s[0] == src:
            dsts = digits_s[1:]
        else:
            dsts = digits_s[:]
        
        dsts.remove(src)
        cnt = 1
        for dst in dsts:
            prime_tmp = prime_s.replace(src, dst)
            if prime_tmp in primes_set:
                cnt += 1
        if cnt>=8:
            print prime, src, cnt
            print "--"
            for dst in dsts:
                prime_tmp = prime_s.replace(src, dst)
                print prime_tmp,
                if prime_tmp in primes_set:
                    print "prime"
                else:
                    print ""

            solved = True
            break

    if solved:
        break
        
            