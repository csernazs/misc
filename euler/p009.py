
import sys
from itertools import combinations, izip
import time

n = int(sys.argv[1])

def get_triplets1(n):
    for a in xrange(1, (n/2)+1):
        for b in xrange(a+1, (n/2)):
            if a == b:
                continue
            c = n - a - b
            if c<1 or b>c:
                break
                
            if c == b or c == a:
                continue
                
            yield (a,b,c)


def get_triplets2(n):
    for a, b, c in combinations(range(1, n+1), 3):
        if a+b+c == n:
            yield (a,b,c)        

def compare(it1, it2):
    for e1, e2 in izip(it1, it2):
        if e1 != e2:
            print e1, e2
            return False
    try:
        it1.next()
    except StopIteration:
        pass
    else:
        return False

    try:
        it2.next()
    except StopIteration:
        pass
    else:
        return False
        
    return True
        

#for a, b, c in get_triplets1(n):
#    print a, b, c

#print compare(get_triplets1(n), get_triplets2(n))

sq = [None]
for i in xrange(1, n+1):
    sq.append(i**2)

sq = tuple(sq)

t1 = time.time()
for a, b, c in get_triplets1(n):
    if sq[a]+sq[b] == sq[c]:
        print a, b, c
        print a*b*c
        break
        
t2=time.time()-t1
print "%s secs %s items/sec" % (t2, n/t2)
#t1 = time.time()
#for i in get_triplets2(n):
#    pass
#t2=time.time()-t1
#print "%s secs %s items/sec" % (t2, n/t2)
