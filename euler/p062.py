
from collections import defaultdict

cache = defaultdict(list)

for i in xrange(10000):
    n = i**3
    n_s=str(n)

    key = [0]*10
    for d in n_s:
        key[int(d)] += 1
    
    key = tuple(key)
    value = cache[key]
    value.append(n)
    if len(value) == 5:
        print value
        print "sol", min(value)
        break

