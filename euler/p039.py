
# pretty inefficient

import math

sqrts = [math.sqrt(x) for x in xrange(2000000+1)]

sqrts = tuple(sqrts)

def solve(perim):

    sol = set()
    
    max_length = perim/2 - 1

    for first in xrange(1, max_length+1):
        for second in xrange(1, max_length+1):
            third = sqrts[first**2+second**2]
            if int(third) == third and first+second+third == perim:
                sol.add(tuple(sorted((first, second, int(third)))))
    
    return sol


max_sol = None
max_len = 0
for perim in xrange(10, 1001):
    print perim
    sol = solve(perim)
    if len(sol) > max_len:
        max_sol = sol
        sol_perim = perim
        max_len = len(sol)

print "--"
print sol_perim
print max_sol

                
        
        