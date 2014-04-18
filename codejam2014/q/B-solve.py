#!/usr/bin/pypy

import sys
infile = sys.argv[1]
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

def solve(price, frate, target):
    time = 0.0
    crate = 2.0
    total = 0.0
    while total<target:
        # buy farm?
        if (target-total-price)/crate > (target-total)/(crate+frate):
            time += price / crate
            crate += frate
        else:	
            time += (target-total)/crate
            total += target-total
        
    return time
    
    
def main():
    f = open(infile, "r")
    no_cases = read_int(f)

    for case_idx in xrange(no_cases):
        price, rate, target = read_floats(f)

        sol = solve(price, rate, target)
        
        out.write("Case #%d: %s\n" % (case_idx+1, round(sol, 7)))
        

if __name__ == "__main__":
    main()
    
    