

import prime


primes = prime.get_primes(1000000)
primes_set = set(map(str, primes))

onedigit_primes = [1,2,3,5,7]
onedigit_primes_set = set(map(str, onedigit_primes))

sum = 0
for num in primes:
#for num in [3797]:

    if num<10:
        continue
        
    num_s = str(num)

    if num_s[-1] not in onedigit_primes_set or num_s[0] not in onedigit_primes_set:
        continue
        

    for idx in xrange(len(num_s)-1, 0, -1):
        if num_s[:idx] not in primes_set:
#            print "2", num
            break
    else:
        for idx in xrange(1, len(num_s)):
            if num_s[idx:] not in primes_set:
#                print "3", num
            
                break
        else:
            print num
            sum += num

    
print "sum", sum