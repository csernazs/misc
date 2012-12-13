
import ctypes

libprime = ctypes.CDLL("./libprime.so")

get_primes_c = libprime.get_primes

is_prime_c = libprime.is_prime

get_primes_c.restype = ctypes.POINTER(ctypes.c_long)

def get_primes(n_max, rettype=list):
    data = get_primes_c(n_max)
    length = data[0]
    if rettype == list:
        return data[1:length+1]        
    elif rettype == set:
        return set(data[1:length+1])

def is_prime(n):
    return is_prime_c(n)

