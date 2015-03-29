#!/usr/bin/pypy

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


def solve():
    pass

if __name__ == "__main__":
    infile = open(sys.argv[1])
    no_cases = int(infile.readline())
    
    
    for cidx in xrange(no_cases):
        sol = solve()
        print "Case #%d: %d" % (cidx+1, sol)
