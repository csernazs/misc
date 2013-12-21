
from __future__ import division

cache = {}

def gcd(a,b):
    if (a,b) in cache:
        return cache[(a,b)]
    else:
      params = (a,b)
          
    while a != b:
        if a>b:
            a = a - b
        else:
            b = b - a
    
    cache[params] = a
    return a      
      
def phi(n):
    cnt = 1
    for i in xrange(2, n):
        if n>i:
          res = gcd(n, i)
        elif n<i:
          res = gcd(i, n)
        else:
          res = i
        
        if res == 1:
            cnt += 1
            
    return cnt
            

#print phi(9)

for i in xrange(2, 1000001):
  res = phi(i)
  print i, res, i/res
