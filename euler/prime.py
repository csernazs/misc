
import time


def get_primes(n):
    numbers = set(xrange(2, n+1))

    n_s = n/2
    for i in xrange(2, n_s):
        if i not in numbers:
#            print "skipping", i
            continue
        t = i*2
        while t<=n:
            numbers.discard(t)
            
            t=t+i
        
    return numbers
    


#get_primes(1000000)


#print "time, number"
#for i in xrange(1000, 100000, 1000):
#    t1=time.time()
#    get_primes(i)
#    t2=time.time()-t1
#    print "%.5f,%d" % (t2, i)
    
    

