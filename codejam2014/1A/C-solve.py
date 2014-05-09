#!/usr/bin/pypy

import sys
infile = sys.argv[1]

import itertools
import random

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


def get_uniform(n):
    retval = range(n)
    for idx in xrange(n):
        cidx = random.randint(idx, n-1)
        retval[idx], retval[cidx] = retval[cidx], retval[idx]
    return retval
    
def get_nonuniform(n):
    retval = range(n)
    for idx in xrange(n):
        cidx = random.randint(0, n-1)
        retval[idx], retval[cidx] = retval[cidx], retval[idx]
    return retval


def solve(data):
    print [sorted([x[0]/10 for x in data]).count(z) for z in xrange(100)]

        
def main():
    f = open(infile, "r")
    no_cases = read_int(f)

    data = []
    for case_idx in xrange(no_cases):
        print "=== CASE", case_idx+1
        no_numbers = read_int(f)
        numbers = read_ints(f)
        data.append(numbers)
    
    solve(data)
        
#        sol = solve(i)
#        out.write("Case #%d: %s %s\n" % (case_idx+1, sol))
        

def summary(data):
    max_num = max(data[0])
    distr = [[x[0] for x in data].count(z) for z in xrange(max_num)]
    print "min", min(distr)
    print "max", max(distr)
    

#def main():
#    print "non-uniform"
#    data_nonunif=[get_nonuniform(1000) for x in xrange(100000)]
#    summary(data_nonunif)
#    del data_nonunif
#
#    print "uniform"
#    data_unif=[get_uniform(1000) for x in xrange(100000)]
#    summary(data_unif)
#    del data_unif
    
    
if __name__ == "__main__":
    main()
    
