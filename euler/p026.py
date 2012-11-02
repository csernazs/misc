
from decimal import Decimal, getcontext
import pdb

import sys

DEBUG = "-d" in sys.argv
def debug(msg):
    if DEBUG:
        print msg
        
def divide(divisor, max_prec=3000):
    debug(">>>> divide %s" % divisor)
    n = 10
    retval = ""

    div, mod = divmod(n, divisor)
    res = div

    if mod == 0:
        return res
    
    prec = 1
    seen = {1: 0, mod: 1}
    debug("STRT div=%d mod=%d res=%d prec=%d" % (div, mod, res, prec))
    start = 0
    while mod != 0 and prec<max_prec:
        div, mod = divmod(mod*10, divisor)
        if res == 0:
            start += 1
        res = res * 10 + div

        if mod in seen:
            prec += 1
            res_s = "0"*start + str(res)
            debug("SEEN div=%d mod=%d res=%d seen[mod]=%d prec=%d str=%s" % (div, mod, res, seen[mod], prec, res_s[seen[mod]:prec]))
            return (res_s, seen[mod], prec)
        else:
            prec += 1
            seen[mod] = prec
            debug("LOOP div=%d mod=%d res=%d prec=%d" % (div, mod, res, prec))

    res_s = "0"*start + str(res)
    return res_s

#print divide(4)

getcontext().prec = 100
one = Decimal(1)

#for i in xrange(2,100):
sol_length = 0

for i in xrange(2, 1000):
#    print "... %d" % i
#    print "=== %s" % (one/Decimal(i))

    sol = divide(i)
    if type(sol) == tuple:
        length = sol[2]-sol[1]
        print i, length
#        print sol[0], sol[0][sol[1]:sol[2]], length
        if length>sol_length:
            sol_length = length
            sol_num = i
        
        

#    else:
#        print sol

    
print "/"*10
print sol_num, sol_length

