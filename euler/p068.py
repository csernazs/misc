

from itertools import *


indexes = ((0,1,2), (3,2,4), (5,4,6), (7,6,8), (9,8,1))

sols = []
for full in permutations([10, 9, 8, 7, 6, 5, 4, 3, 2, 1], 10):
#    full = (9,) + full

    tmpsum = sum(full[:3])
#    print tmpsum
    for idx in indexes[1:]:
        if sum([full[i] for i in idx]) != tmpsum:
            break
    else:
        #print "-"*50
        #print full, tmpsum
        sol = []
        for idx in indexes:
            sol.append([full[i] for i in idx])
#            print "".join(map(str, full))


        minsol = min(sol)
        minidx = sol.index(minsol)


        
        #print "A", sol
        sol = sol[minidx:] + sol[:minidx]
        #print "B", sol

        sol_s = "".join(["".join(map(str, x)) for x in sol])
        if len(sol_s) == 16:
            sols.append(sol_s)

#print sorted(set(sols))
#print "---"
print max(sols)
        
