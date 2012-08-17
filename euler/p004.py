

import itertools
results = set()

for op1, op2 in itertools.combinations_with_replacement(xrange(999, 100, -1), 2):
    res = op1 * op2
    res_s = str(res)

    if res_s == res_s[::-1]:
        results.add(res)

print max(results)

