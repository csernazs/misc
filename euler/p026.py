
import largest
from decimal import Decimal, getcontext

getcontext().prec = 1000
one = Decimal(1)
import re

sol_l = 0
sol = None
idx = None

for i in xrange(1, 1001):
    print i, sol
    result = one / Decimal(i)
    result_s = str(result)[2:-1]
    if not result_s:
        continue
        
    tmp = largest.find_largest_cycle(result_s)
    if len(tmp)>sol_l:
        sol_l = len(tmp)
        sol = tmp
        idx = i
        
    
        
    
print idx
print sol
print sol_l

