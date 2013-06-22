
from collections import defaultdict


gen = [lambda n: n*(n+1)/2,
        lambda n: n**2,
        lambda n: n*(3*n-1)/2,
        lambda n: n*(2*n-1),
        lambda n: n*(5*n-3)/2,
        lambda n: n*(3*n-2)]
       
       
data = []

for func in gen:
    n=1
    curr = defaultdict(list)
    while True:
        item = func(n)
        if item<1000:
            n += 1
            continue
            
        if item>=10000:
            break
        
        item_s = str(item)
        curr[item_s[:2]].append(item_s)
        
        n += 1
        
    data.append(curr)
    

def solve(data, free, sol, max_sol):
    if len(sol) == max_sol:
        print "final", sol
        if sol[0][:2] == sol[-1][-2:]:
            return True
        else:
            return False
        
    for didx in free:
        domain = data[didx]
        for key, value in domain.iteritems():
            for num in value:
                if len(sol) == 0:
                    sol.append(num)
                else:
                    if sol[-1][-2:] == num[:2]:
                        sol.append(num)
                    else:
                        continue

                print "try", sol
                if not solve(data, free-set([didx]), sol, max_sol):
                    sol.pop(-1)
                else:
                    return True
    return False
                    

sol = []
print solve(data, set(range(len(data))), sol, 6)
print sol
print sum(map(int, sol))
