#!/usr/bin/pypy

from itertools import *
import sys
import time
import math

def read_int(f):
    return int(f.readline())

def read_ints(f, sep=" "):
    return map(int, f.readline().rstrip().split(sep))

def read_lines(f, no_lines):
    retval = []
    for i in xrange(no_lines):
        retval.append(f.readline().rstrip())
    return retval



def palindrome_gen_l(length):
    if length == 1:
        for i in xrange(1, 10):
            yield i
        return
        
            
    l_2 = length / 2
    odd = length % 2
    
    mul = [10**x for x in xrange(length-1, -1, -1)]
    
    def get_number(digits):
        retval = 0
        for d, m in zip(digits, mul):
            retval += d*m
        return retval
        
    for digits in product(range(10), repeat=length/2):
        if digits[0] == 0:
            continue
            
        if odd:
            for i in xrange(10):
                num = digits + (i,) + tuple(reversed(digits))
                yield get_number(num)
        else:
            num= digits + tuple(reversed(digits))
            yield get_number(num)
        
def palindrome_gen(a, b):
    l_min = len(str(a))
    l_max = len(str(b))
    gchain = []
    for i in xrange(l_min, l_max+1):
        gchain.append(palindrome_gen_l(i))
    
    for num in chain(*gchain):
        if num<a:
            continue
        if num>b:
            break
        yield num

    
def is_palindrome(n):
    if n<10 and n>0:
        return True
    n_s = str(int(n))
    for a, b in zip(n_s, reversed(n_s)):
        if a!=b:
            return False
            
    return True
        
def solve(low, high):
    #print "===", low, high

    range_s = int(math.sqrt(low))
    range_e = int(math.sqrt(high))
    

    cnt = 0
    for pal in palindrome_gen(range_s, range_e):
        pal_2 = pal**2
        #print "?", pal, pal_2

        if pal_2 <= high and pal_2>=low and is_palindrome(pal_2):
            #print pal, pal_2
            cnt += 1    
    
    return cnt
    
if __name__ == "__main__":
    infile = open(sys.argv[1])
    no_cases = int(infile.readline())
    
    for cidx in xrange(no_cases):
        low, high = read_ints(infile)
        sol = solve(low, high)

        print "Case #%d: %d" % (cidx+1, sol)
