
import c_prime
primes = c_prime.get_primes(1000000)
primes_set = set(primes)

from collections import deque, defaultdict

def get_factors(n):
    retval = []
    factors = defaultdict(int)
    for prime in primes:
        if n == 1:
            break
            
        if n == prime:
            factors[n] = 1
            break
            
        while 1:
            div, mod = divmod(n, prime)
            if mod == 0:
                n = div
#                print n, prime
                factors[prime] += 1
                
            else:
                break
                
    return factors.items()
    

print get_factors(14)
print get_factors(15)
print get_factors(644)

n = 12
numbers = deque()
length = 4
solved = False
while not solved:
    if n % 1000 == 0:
        print n
    if n > primes[-1]:
        break
        
    if n in primes_set:
        n += 1
        numbers = deque()
        continue
        
    if len(numbers) < length:
        numbers.append((n, get_factors(n)))

    if len(numbers) == length:
        for num, fact in numbers:
            if len(fact) != length:
                break
                
        else:
            print "found", [x[0] for x in numbers]
            solved = True
        
        numbers.popleft()
    
#    print time.time()-t1
    n += 1
#    print "-"*30
    