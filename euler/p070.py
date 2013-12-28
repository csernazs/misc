
from __future__ import division

from math import sqrt
import prime

MAX=10000000

min_range = int(sqrt(MAX)*0.5)
max_range = int(sqrt(MAX)*1.5)

print "min_range", min_range
print "max_range", max_range

primes = [x for x in prime.get_primes(max_range) if x>min_range]

print primes

def is_perm(a, b):
    a_s = str(a)
    b_s = str(b)
    if len(a_s) != len(b_s):
        return False
        
    if set(a_s) != set(b_s):
        return False
        
    a_digits = [0]*58
    b_digits = [0]*58
    
    for digit in a_s:
        a_digits[ord(digit)] += 1

    for digit in b_s:
        o_digit = ord(digit)
        b_digits[o_digit] += 1
        if a_digits[o_digit]<b_digits[o_digit]:
            return False
    return a_digits == b_digits
    


ratio = float("inf")
print "i,j,n,phi,ratio"
for iidx, i in enumerate(primes):
    for j in primes[iidx-1:]:
        n = i*j
        if n>MAX:
            break
        phi = (i-1)*(j-1)
        new_ratio = n/phi
        if new_ratio < ratio and is_perm(phi, n):
            ratio = new_ratio
            print i,j,n,phi, ratio
        
        