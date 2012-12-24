
n = 2
numbers = [1]
n_set = set(numbers)

import math

def is_penta(x):
    return (1+math.sqrt(1-12*(-2*x))) % 6 == 0

found = False
while not found:
    pn = n*(3*n-1)/2
    for prev in numbers:
        if (pn-prev in n_set or abs(prev-pn) in n_set) and is_penta(pn+prev):
            print pn, prev, pn-prev
            found = True
            break
    else:
        numbers.append(pn)
        n_set.add(pn)
        n = n + 1
    