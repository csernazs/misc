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


def solve(me, others):
    me_orig = me
    others = sorted(others)
    others_orig = others[:]

#    print me, others

    if me>others[-1]:
        return 0
    
    removed = False
    for other in others[:]:
        if other < me:
            me += other
            others.remove(other)
            removed = True

    if len(others) == 0:
        return 0

    if len(others) == 1:
        return 1
    
    if me == 1:
        return len(others)

    sol1 = len(others)
    sol2 = solve(me_orig, [me-1]+others_orig)+1
    if sol1<sol2:
        return sol1
    else:
        return sol2

    
if __name__ == "__main__":
    infile = open(sys.argv[1])
    no_cases = int(infile.readline())
    
    
    for cidx in xrange(no_cases):
        me, others_len = read_ints(infile)
        others = read_ints(infile)
        
#        print "-"*100
        sol = solve(me, others)
        print "Case #%d: %d" % (cidx+1, sol)
