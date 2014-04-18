#!/usr/bin/pypy

import sys
import itertools

infile = sys.argv[1]
try:
    out = open(sys.argv[2], "w")
except IndexError:
    out = sys.stdout

def read_int(f):
    return int(f.readline())

def read_ints(f, sep=" "):
    return map(int, f.readline().rstrip().split(sep))

def read_lines(f, no_lines):
    retval = []
    for i in xrange(no_lines):
        retval.append(f.readline().rstrip())
    return retval


def print_field(f):
    retval = []
    for row in f:
        retval.append("".join(row))
    return "\n".join(retval)

def calc_cell(field, row_idx, col_idx):
    retval = 0
    rows = len(field)
    cols = len(field[0])
    
    for roffset in [-1, 0, 1]:
        for coffset in [-1, 0, 1]:
            if row_idx+roffset < 0 or col_idx+coffset < 0:
                continue
                
            if roffset==0 and coffset == 0:
                continue

            try:
                if field[row_idx+roffset][col_idx+coffset] == "*":
                    retval += 1
            except IndexError:
                pass

    return retval

def count(field, cell):
    retval = 0
    for row in field:
        retval += row.count(cell)
    return retval

def walk(field, rowidx, colidx):
    if rowidx<0 or colidx<0:
        return
    try:
        val = field[rowidx][colidx]
    except IndexError:
        return
        
    if val == " ":
        new_val = calc_cell(field, rowidx, colidx)
        if new_val == 0:
            field[rowidx][colidx] = "."
            walk(field, rowidx-1, colidx)
            walk(field, rowidx+1, colidx)

            walk(field, rowidx, colidx-1)
            walk(field, rowidx, colidx+1)

            walk(field, rowidx-1, colidx-1)
            walk(field, rowidx+1, colidx+1)
            
            walk(field, rowidx-1, colidx+1)
            walk(field, rowidx+1, colidx-1)
        else:
            field[rowidx][colidx] = str(new_val)
        

def check(field, rowidx, colidx):
    walk(field, rowidx, colidx)
    print "check", rowidx, colidx
    print print_field(field)
#    if field[rowidx][colidx] == ".":       
#        field[rowidx][colidx] = "c"

    if field[rowidx][colidx] in "12345678":
        if count(field, " ")>0:
            print False
            return False
        else:
            print True
            return True

    if count(field, " ") > 0:
        print False
        return False
        
    print True
    return True

def copy(field):
    retval = []
    for row in field:
        retval.append(row[:])
    return retval

def next(field):
    rows = len(field)
    cols = len(field[0])
    
    for row_no in xrange(rows):
        for col_no in xrange(cols):
            curr = field[row_no][col_no]
            if curr == " ":
                new = copy(field)
                new[row_no][col_no] = "*"
                possible = check(new, rows-1, cols-1)
                if possible:
                    field[row_no][col_no] = "*"
                    return True
        
    return False
        
def solve(rows, cols, mines):
    print "solve", rows, cols, mines


    field = [[" "]*cols for x in xrange(rows)]

    cnt = 0

    while cnt < mines:
        status = next(field)
        if status:
            cnt += 1
        else:
            return "Impossible"
    
    field[-1][-1] = "c"
    return print_field(field)            
    
        
def main():
    f = open(infile, "r")
    no_cases = read_int(f)

    
    for case_idx in xrange(no_cases):
        rows, cols, mines = read_ints(f)
        
        sol = solve(rows, cols, mines)
#        for char in "12345678 ":
#            sol = sol.replace(char, ".")

        for char in " ":
            sol = sol.replace(char, ".")
            
        out.write("Case #%d:\n%s\n" % (case_idx+1, sol))
        

if __name__ == "__main__":
    main()
    
    