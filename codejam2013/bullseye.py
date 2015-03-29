#!/usr/bin/pypy -u

import sys

def read_int(f):
    return int(f.readline())

def read_ints(f, sep=" "):
    return map(int, f.readline().rstrip().split(sep))

def read_lines(f, no_lines):
    retval = []
    for i in xrange(no_lines):
        retval.append(f.readline().rstrip())
    return retval


def iter_rings(radius):

    while True:
        inner_area = radius**2
        outer_area = (radius+1)**2
        yield outer_area-inner_area
        radius += 2
        
def solve(init, paint):
    i1 = (init+1)**2
    i2 = init**2
    i3 = i1-i2


    lo, hi = 0, 100000

    a1 = i3

    while True:
        n = lo+(hi-lo)/2
        an = a1 + (n-1)*4
        s = ((a1+an)*n) / 2

        if s<paint:
            n = n / 2
        else:
            n = n+ (n * 2 - n) / 2
                

if __name__ == "__main__":
    infile = open(sys.argv[1])
    no_cases = int(infile.readline())
    
    
    for cidx in xrange(no_cases):
        init, paint =read_ints(infile)
        sol = solve(init, paint)
        print "Case #%d: %d" % (cidx+1, sol)
