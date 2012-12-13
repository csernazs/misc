
import sys
import c_prime

from itertools import permutations

"""
for num in xrange(987654321, 123456789-1, -2):
    num_s = str(num)
    if "0" in num_s:
        continue
    
    if sum(map(int, num_s)) == 3:
        continue
        
    if len(set(num_s)) == len(num_s):
        print num
        if c_prime.is_prime(num):
            break
"""


def solve(length):
    odd = set(("1","3","5","7","9"))
    
    retval = None
    for digits in permutations(map(str, range(1,length+1)), length):
        if digits[-1] in odd and len(set(digits)) == length:
            num = int("".join(digits))
            if num>retval and c_prime.is_prime(num):
                retval = num
                
    return retval
    

for i in xrange(9, 1, -1):
    print i
    res = solve(i)
    if res:
        print res
        break
        

