
import ctypes

libprime = ctypes.CDLL("./libprime.so")

get_primes_c = libprime.get_primes

get_primes_c.restype = ctypes.POINTER(ctypes.c_int)

def get_primes(n_max, rettype=list):
    if rettype == list:
        retval = []
        for i in get_primes_c(n_max):
            if i == 0:
                break
            retval.append(i)
    elif rettype == set:
        retval = set()
        for i in get_primes_c(n_max):
            if i == 0:
                break
            retval.add(i)
    
    return retval
    
    

