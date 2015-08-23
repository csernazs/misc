#!/usr/bin/pypy

from collections import defaultdict

def gcd(a,b):
    while b != 0:
        a, b = b, a % b
    return a

def main():
    MAX = 1000
    LIMIT = 1500000
    
    triangles = defaultdict(list)
    
    for n in xrange(1, MAX):
#        print n
        for m in xrange(n+1, MAX, 2):
            if gcd(m, n) != 1:
                continue
                
            a = m**2 - n**2
            b = 2 * m * n
            c = m**2 + n**2
            
#            print "-"*10
#            print "n", n
#            print "m", m
#            assert a**2+b**2 == c**2
            
            perimeter = a + b + c
            if perimeter<=LIMIT:
                triangles[perimeter].append((a,b,c))
            else:
#                print "limit", n, m
                break
                
#            print (a,b,c), a+b+c
    tr_copy = triangles.copy()
    
    for idx, primitives in enumerate(tr_copy.itervalues()):
#        print idx
        for p in primitives:
            mul = 2
            while True:
                new = (p[0] * mul, p[1] * mul, p[2] * mul)
                perimeter = new[0] + new[1] + new[2]
                if perimeter <= LIMIT:
                    triangles[perimeter].append(new)
                    mul += 1
                else:
                    break
    
    del tr_copy
    
    cnt = 0
    for value in triangles.itervalues():
        if len(value) == 1:
            cnt += 1
        
    print "sol", cnt
if __name__ == "__main__":
    main()

            