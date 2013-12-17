

import math

print "pre-calc"

def get_squares():
    n = 0
    while True:
        yield n*n
        n += 1
        
def get_D():
    a = 2
    while True:
        c = math.sqrt(a)
        if c != int(c):
            yield a
        a += 1
        

x_max = 0
sol_D = None

print "pre-calc done"

cache = {}
def sqrt(n):
    retval = cache.get(n)    
    if retval is None:
        retval = math.sqrt(n)
        cache[n] = retval
        return retval
    else:
        return retval
                
for D in get_D():
    if D>1000:
        break

    for x, x_sq in enumerate(get_squares()):
        if x < 1:
            continue

        if x%10000000 == 0:
            print x
            
        key, mod = divmod(x_sq-1, D)
        if mod != 0 or key == 0:
            continue


        y = math.sqrt(key)
        
        if y == int(y):
            y = int(y)
#            print "x, D, y", x, D, y
            print "%d^2 - %d*%d^2" % ( x, D, y)
            if x>x_max:
                x_max = x
                sol_D = D
            break
    else:
        raise ValueError("No solution for D=%d" % D)

print "x_max", x_max
print "sol", sol_D
