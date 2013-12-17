

import math

print "pre-calc"

squares = tuple([x**2 for x in xrange(10000000)])
squares_set = set(squares)
squares_max = squares[-1]


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

for D in get_D():
    if D>1000:
        break
#    if D!=61:
#        continue

    for x, x_sq in enumerate(squares):
        if x < 1:
            continue

#        y_sq = (x_sq-1)/(D*1.0)
        
#        if int(y_sq) == y_sq and math.sqrt(y_sq) == int(math.sqrt(y_sq)):
#            print x_sq, y_sq, D
        
#        assert round(x_sq - D*y_sq, 5) == 1
        
        key, mod = divmod(x_sq-1, D)
        if mod != 0 or key == 0:
            continue

    
        if key > squares_max:
            raise ValueError("key=%d, max=%d" % (key, squares_max))

        if key in squares_set:
            y = squares.index(key)
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
