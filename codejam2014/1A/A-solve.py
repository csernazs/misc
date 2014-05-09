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


def solved(outlets, devices):
    for dev in devices:
        if dev not in outlets:
            return False
    return True

def apply_switch(outlets, switch):
    length = len(outlets[0])
    retval = [outlet[:] for outlet in outlets]

    for idx, sw in enumerate(switch):
        if sw == 0:
            continue
        
        for outlet, ret in zip(outlets, retval):
            ret[idx] = int(not outlet[idx])
    
    return retval
    
def solve(outlets, devices):
    #print "outlets", outlets
    #print "devices", devices


    if solved(outlets, devices):
        #print "already solved"
        return 0
            
    for dev in devices:
        if dev in outlets:
            continue
        else:
            #print "mismatch", dev, outlets
            switches=[]
            for outlet in outlets:
                switch = map(lambda xy: int(xy[0]!=xy[1]), zip(outlet, dev))
                #print "switch", dev, outlet, switch
                switches.append(switch)
                
            switches.sort(key=lambda x: x.count(1))
            
            #print "swithes", switches
            for switch in switches:
                new_outlets = apply_switch(outlets, switch)
                if solved(new_outlets, devices):
                    #print "solution", outlets, devices, switch, switch.count(1)
                    return switch.count(1)
                    
            
            return "NOT POSSIBLE"
        
    
def main():
    f = open(infile, "r")
    no_cases = read_int(f)

    for case_idx in xrange(no_cases):
        f.readline()
        outlets = [map(int, x) for x in f.readline().strip().split(" ")]
        devices = [map(int, x) for x in f.readline().strip().split(" ")]
        print "CASE", case_idx+1
        sol = solve(outlets, devices)
        out.write("Case #%d: %s\n" % (case_idx+1, sol))
        

if __name__ == "__main__":
    main()
    
