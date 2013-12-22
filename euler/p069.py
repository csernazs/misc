
from __future__ import division

def gcd(a,b):
    while b != 0:
        a, b = b, a % b
    return a
          
def phi(n):
    cnt = 1
    for i in xrange(2, n):
        res = gcd(n, i)
        if res == 1:
            cnt += 1
    return cnt
            

maxres = 0
primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
primes_i = iter(primes)

i = 210
maxres = 0

while True:
  i = i * primes_i.next()
  if i > 1000000:
    break
  res = phi(i)
  divres = i / res
  if divres>maxres:
    print i, res, divres
    maxres = divres
  
