
import time
import tempfile
import os
pjoin = os.path.join
import cPickle

from array import array


path_template = pjoin(tempfile.gettempdir(), "primes_%d.txt")

def get_primes(n):
    path = path_template % n
    if os.path.isfile(path):
        return map(int, open(path).read().split(" "))

    t1=time.time()
#    numbers = array("B", [0]*(n+1));
    numbers = [0]*(n+1);
    
    #xrange(2, n+1))

    n_s = n/2
    for i in xrange(2, n_s):
        if numbers[i] == 1:
#            print "skipping", i
            continue
        t = i*2
        while t<=n:
            numbers[t] = 1;
            t=t+i


    retval = []
    for idx, x in enumerate(numbers):
        if idx<2:
            continue
        if x == 0:
            retval.append(idx)

    open(path, "w").write(" ".join(map(str, retval)))
    return retval
    

if __name__ == "__main__":
    print get_primes(1000000)[:100]


#print "time, number"
#for i in xrange(1000, 100000, 1000):
#    t1=time.time()
#    get_primes(i)
#    t2=time.time()-t1
#    print "%.5f,%d" % (t2, i)
    
    

