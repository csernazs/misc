#!/usr/bin/pypy

import sys
infile = sys.argv[1]
try:
    outfile = sys.argv[2]
except IndexError:
    outfile = sys.stdout

def read_int(f):
    return int(f.readline())

def read_ints(f, sep=" "):
    return map(int, f.readline().rstrip().split(sep))

def read_lines(f, no_lines):
    retval = []
    for i in xrange(no_lines):
        retval.append(f.readline().rstrip())
    return retval

def solve(rows, datas):
    first = set(datas[0][rows[0]-1])
    second = set(datas[1][rows[1]-1])
    
    match = first.intersection(second)
    
    if len(match) == 0:
        return "Volunteer cheated!"
    if len(match) == 1:
        return str(list(match)[0])
    else:
        return "Bad magician!"
        
    
    
def main():
    f = open(infile, "r")
    no_cases = read_int(f)

    out = open(outfile, "w")
    
    for case_idx in xrange(no_cases):
        rows = []
        datas = []
        for z in xrange(2):
            row_no = read_int(f)
            data = []
            for x in xrange(4):
                data.append([int(x) for x in f.readline().split(" ")])
            print row_no
            print data

            rows.append(row_no)
            datas.append(data)
        
        out.write("Case #%d: %s\n" % (case_idx+1, solve(rows, datas)))
        

if __name__ == "__main__":
    main()
    
    