
import c_prime

primes = c_prime.get_primes(1000000)
primes_set = set(primes)

res = []
for start in xrange(len(primes)):
    for end in xrange(start+1, len(primes)):
        s = sum(primes[start:end])
        if s>1000000:
            break
        if s in primes_set:
#            print primes[start:end]
#            print s
            res.append((primes[start:end], s))
            
res.sort(lambda x, y: cmp(len(x[0]), len(y[0])))

print res[-1]
