from fractions import Fraction as F




x = F(1, 2+F(1,2))


cnt = 0
for i in xrange(1000):
    x = F(1, 2+x)
    t = 1+x
    if len(str(t.numerator)) > len(str(t.denominator)):
#        print t
        cnt += 1


print cnt
