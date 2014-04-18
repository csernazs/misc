#!/usr/bin/pypy

import sys
infile = sys.argv[1]

from bisect import bisect_right
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


def find_gt(a, x):
    'Find leftmost value greater than x'
    i = bisect_right(a, x)
    if i != len(a):
        return i
    return None

def play_war(naomi, ken):
    score = 0
    while len(naomi)>0:
        n_mass = naomi.pop(0)
        k_idx = find_gt(ken, n_mass)
        if k_idx is None:
            k_mass = ken.pop(0)
        else:
            k_mass = ken.pop(k_idx)
            
        if n_mass>k_mass:
            score += 1
    return score

epsilon = 0.000001


def play_dwar(naomi, ken):
    score = 0
    while len(naomi)>0:
        print "naomi", naomi
        print "ken  ", ken
        
        nidx = find_gt(naomi, ken[0])
        if nidx: # lie that we have the largest
            n_told = ken[-1]+1
            n_mass = naomi.pop(nidx)
        elif naomi[-1] > ken[-1]: # no lie
            n_mass = naomi.pop()
            n_told = n_mass
        else:  # lie and lose
            n_mass = naomi.pop(0)
            n_told = ken[-1]-epsilon

        print "n_mass", n_mass
        print "n_told", n_told
        
        k_idx = find_gt(ken, n_told)
        if k_idx is None:
            k_mass = ken.pop(0)
        else:        
            k_mass = ken.pop(k_idx)

        print "k_mass", k_mass
        
        if n_mass>k_mass:
            score += 1
            print "win", score

        else:
            print "lose", score
    
    return score
            

def solve(naomi, ken):
    naomi.sort()
    ken.sort()
    
    z = play_war(naomi[:], ken[:])

#    y_max = 0
    y_max = play_dwar(naomi[:], ken[:])

#    patterns = itertools.product([True, False], repeat=10)
#    for pattern in patterns:
#        y = play_dwar(naomi[:], ken[:], pattern)
#        if y>y_max:
#            y_max = y
#
    return (y_max, z)
    
    
def main():
    f = open(infile, "r")
    no_cases = read_int(f)

    for case_idx in xrange(no_cases):
        no_masses = read_int(f)
        naomi = read_floats(f)
        ken = read_floats(f)
        assert len(naomi) == no_masses
        assert len(ken) == no_masses
            
        sol = solve(naomi, ken)
        
        out.write("Case #%d: %s %s\n" % (case_idx+1, sol[0], sol[1]))
        

if __name__ == "__main__":
    main()
    
    