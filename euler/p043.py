

import itertools

res = []
for d in itertools.permutations(range(10), 10):
    if d[0] is 0:
        continue
        
    if (d[1]*100+d[2]*10+d[3]) % 2 == 0 and \
        (d[2]*100 + d[3]*10 + d[4]) % 3 == 0 and \
        (d[3]*100 + d[4]*10 + d[5]) % 5 == 0 and \
        (d[4]*100 + d[5]*10 + d[6]) % 7 == 0 and \
        (d[5]*100 + d[6]*10 + d[7]) % 11 == 0 and \
        (d[6]*100 + d[7]*10 + d[8]) % 13 == 0 and \
        (d[7]*100 + d[8]*10 + d[9]) % 17 == 0:
    
        num = sum([d[i]*10**(10-i-1) for i in xrange(10)])
        print num
        res.append(num)

print "--"
print sum(res)    