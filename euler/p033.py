
from fractions import Fraction

digits = range(1, 10)
print digits

sol = 1

for first in digits:
    for second in digits:
        if second == first:
            continue
            
        num = first*10 + second
        
        for third in digits:
            denums = [second*10 + third, third*10 + second]

            for denum in denums:
                res1 = num/(denum*1.0)
                if res1>=1:
                    continue
                    
                res2 = first/(third*1.0)
                if res1 == res2:
                    print num, denum
                    sol *= Fraction(num, denum)
                    
print "sol: ", sol
            
