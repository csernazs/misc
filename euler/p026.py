

from decimal import Decimal, getcontext

getcontext().prec = 1000
one = Decimal(1)
import re

sol_l = 0
sol = None

for i in xrange(1, 1001):
#    print i
    result = one / Decimal(i)
    result_s = str(result)[2:-1]
#    print i, result_s 
    if not result_s:
        continue
        
    for idx in xrange(len(result_s)/2, 2, -1):
        if result_s[:idx] == result_s[idx:idx*2]:
            tmp = result_s[:idx]
            break
            
            
    print i, len(tmp)
    if i == 997:
        print result_s
    if len(tmp)>sol_l:
        sol_l = len(tmp)
        sol = (result, tmp, sol_l, i)

print sol
