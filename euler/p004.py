

import itertools

results = []

for op1, op2 in itertools.combinations_with_replacement(xrange(999, 0, -1), 2):
    res = str(op1 * op2)
    
    if len(res) % 2 == 0:
        left = res[:len(res)/2]
        right = res[:0-(len(res)/2+1):-1]
        if left == right:
            results.append(int(res))
            
print max(results)

