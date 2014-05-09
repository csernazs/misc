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

def counter(symbols):
    length = len(symbols)
    indexes = [0]*length
    lengths = [len(x) for x in symbols]
    if 0 in lengths:
        return

    yield [symbols[idx][indexes[idx]] for idx, iidx in enumerate(indexes)]
    
    while True:
        for iidx in xrange(length-1, -1, -1):
            if indexes[iidx]<lengths[iidx]-1:  
                indexes[iidx] += 1
                break
            else:
                indexes[iidx] = 0

        else:
            break
            
        yield [symbols[idx][iidx] for idx, iidx in enumerate(indexes)]



def solved(strings):
    ref = strings[0]
    for test in strings[1:]:
        if test != ref:
            return False
    return True

def get_pattern(string):
    rep_char = None
    retval = []
    for char in string:
        if rep_char is None:
            rep_char = char
            cnt = 1
            continue
        
        if char == rep_char:
            cnt += 1
        else:
            retval.append([cnt, rep_char])
            rep_char = char
            cnt = 1

    retval.append([cnt, rep_char])
    return retval            
    

def can_solved(patterns):
    ref = [x[1] for x in patterns[0]]
    #print ref
    
    for pattern in patterns[1:]:
        test = [x[1] for x in pattern]
        if test != ref:
            return False
    
    return True
        
    
def solve(strings):
    if solved(strings):
        return 0

    patterns = []        
    for string in strings:
        patterns.append(get_pattern(string))

        
    solvable = can_solved(patterns)
    if not solvable:
        return "Fegla Won"
        

    mincost = 10**100
    mins = {}
    maxs = {}
    for pattern in patterns:
        for value, key in pattern:
            if key not in mins:
                mins[key] = value
            elif value<mins[key]:
                mins[key] = value
            
            if key not in maxs:
                maxs[key] = value
            elif value>maxs[key]:
                maxs[key] = value

    #print "mins", mins
    #print "maxs", maxs                

    minpattern = []
    maxpattern = []
#    symbols = []
    for char in [x[1] for x in patterns[0]]:
        minpattern.append([mins[char], char])
        maxpattern.append([maxs[char], char])

#        symbols.append(range(mins[char], maxs[char]))
    #print "minpattern", minpattern
    #print "maxpattern", maxpattern

    refpatterns = [x[:] for x in patterns]
    if minpattern not in refpatterns:
        refpatterns.append(minpattern)
    if maxpattern not in refpatterns:
        refpatterns.append(maxpattern)


#    for counts in counter(symbols):
#        refpattern = []
#        for count, pattern in zip(counts, patterns[0]):
#            refpattern.append([count, pattern[1]])
#        
#        if refpatterns not in refpatterns:
#            refpatterns.append(refpattern)
    
    for refpattern in refpatterns:
        ref = [x[0] for x in refpattern]
        cost = 0
        for pattern in patterns:
            reps = [x[0] for x in pattern]
            if ref != reps:
                for a, b in zip(ref, reps):
                    cost += abs(a-b)
        if cost < mincost:
            mincost = cost
            
    return mincost
        
    
def main():
    f = open(infile, "r")
    no_cases = read_int(f)

    for case_idx in xrange(no_cases):
        no_strings = read_int(f)
        strings = []
        for string_idx in xrange(no_strings):
            strings.append(f.readline().strip())

        sol = solve(strings)
        out.write("Case #%d: %s\n" % (case_idx+1, sol))
        

if __name__ == "__main__":
    main()
    
