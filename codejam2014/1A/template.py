#!/usr/bin/pypy

import sys
infile = sys.argv[1]

import itertools

try:
    out = open(sys.argv[2], "w")
except IndexError:
    out = sys.stdout

def read_int(f):
    return int(f.readline())

def read_ints(f, sep=" "):
    return map(int, f.readline().rstrip().split(sep))

def read_floats(f, sep=" "):
    return map(float, f.readline().rstrip().split(sep))

def read_lines(f, no_lines):
    retval = []
    for i in xrange(no_lines):
        retval.append(f.readline().rstrip())
    return retval


def solve(input):
    pass
    
    
def main():
    f = open(infile, "r")
    no_cases = read_int(f)

    for case_idx in xrange(no_cases):

        
        sol = solve(i)
        out.write("Case #%d: %s %s\n" % (case_idx+1, sol))
        

if __name__ == "__main__":
    main()
    
