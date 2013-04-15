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

def print_mow(mow):
    print "-"*10
    for row in mow:
        print " ".join(["%3d" % x for x in row])

def solve(tmow, height, width):
    if width == 1 or height == 1:
        return "YES"

    max_c = max([max(row) for row in tmow])
    min_c = min([min(row) for row in tmow])

    #print "max, min", max_c, min_c
    
    cmow = [[max_c]*width for x in xrange(height)]

    #print_mow(tmow)    
    for mv in xrange(max_c-1, min_c-1, -1):
        #print "mv", mv
        for ridx, row in enumerate(tmow):
            if max(row)<=mv:
                for cidx, c in enumerate(cmow[ridx]):
                    if cmow[ridx][cidx]>=mv:
                        cmow[ridx][cidx] = mv
        
        for cidx in xrange(width):
            col = [row[cidx] for row in tmow]
            if max(col)<=mv:
                for ridx, row in enumerate(cmow):
                    row[cidx] = mv

        #print_mow(cmow)    

    if cmow == tmow:
        return "YES"
    else:
        return "NO"        



if __name__ == "__main__":
    infile = open(sys.argv[1])
    no_cases = int(infile.readline())
    
    
    for cidx in xrange(no_cases):
        
        height,width = read_ints(infile)
        mow = []
        for rowidx in xrange(height):
            mow.append(read_ints(infile))

        sol = solve(mow, height, width)

        print "Case #%d: %s" % (cidx+1, sol)
