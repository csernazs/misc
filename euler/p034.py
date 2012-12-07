
from itertools import product


fracts = [1, 1]
for i in xrange(2, 10):
    fracts.append(fracts[-1]*i)

fracts = tuple(fracts)    

def solve(length):
    print "solve", length
    num = 0
    retval = []
    for digits in product(range(10), repeat=length):
        if digits[0] > 0:
            res = 0
            for d in digits:
                res += fracts[d]
                if res>num:
                    break
            else:
                if num == res:
                    print num
                    retval.append(num)

        num = num + 1

    return retval


for length in xrange(2, 8):
    solve(length)
    
