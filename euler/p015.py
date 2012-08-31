
# 6
# 20
# 70
# 252



from math import factorial

def solve(n):
    return factorial(n*2) / factorial(n)**2
    
for i in xrange(2, 21):
    print i, solve(i)
