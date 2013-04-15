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

def check_rows(board, winners):
    print "--"
    print_board(board)
    for row in board:
        if "T" in row:
            req = 3
        else:
            req = 4
        if row.count("O") == req:
            winners.add("O")
        if row.count("X") == req:
            winners.add("X")

def print_board(board):
    for row in board:
        print "".join(row)
        
def solve(board):
    #print "="*20
    #print_board(board)
    
    winners = set()
    
    check_rows(board, winners)
    check_rows(zip(*board), winners)
    
    trow1 = []
    trow2 = []
    for i in xrange(4):
        trow1.append(board[i][i])
        trow2.append(board[3-i][i])
    check_rows([trow1, trow2], winners)
    
    if "X" in winners and "O" in winners:
        return "Draw"
    if "X" in winners:
        return "X won"
    if "O" in winners:
        return "O won"

    completed = True
    for row in board:
        if "." in row:
            completed = False
            break
        
    if completed:
        return "Draw"
    else:
        return "Game has not completed"
    
    

if __name__ == "__main__":
    infile = open(sys.argv[1])
    no_cases = int(infile.readline())

    for cidx in xrange(no_cases):
        
        board = []
        for i in xrange(4):
            row = list(infile.readline().strip())
            board.append(row)
        
        infile.readline()
        sol = solve(board)
        
        print "Case #%d: %s" % (cidx+1, sol)
