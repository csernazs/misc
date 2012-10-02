
from itertools import islice, takewhile, product

def get_abundant_numbers():
    n = 12
    while True:
        div_sum = 0
        print n
        for t in xrange(n/2, 0, -1):
            if n%t == 0:
#                print n, t
                div_sum += t
            if div_sum>n:
#                yield (n, div_sum)
                yield n
                break

        n+=1


print 1
numbers = list(takewhile(lambda x: x<28123, get_abundant_numbers()))
print 2

results = [False] * 28124
for a, b in product(numbers, repeat=2):
    s = a+b
    if s<=28123:
        results[s] = True
print 3

result = 0        
for idx, n in enumerate(results):
    if not n:
        print idx
        result += idx

print "result"
print result

        