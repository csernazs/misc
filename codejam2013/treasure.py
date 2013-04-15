#!/usr/bin/pypy -u

import time
from collections import defaultdict
import pdb
from array import array

import sys

def read_int(f):
    return int(f.readline())

def read_ints(f, sep=" "):
    return map(int, f.readline().rstrip().split(sep))

def read_lines(f, no_lines, type=str):
    retval = []
    for i in xrange(no_lines):
        retval.append(type(f.readline().rstrip()))
    return retval

class Chest(object):
    def __init__(self, idx, lock, keys=None, opened=False):
        self.idx = idx
        self.lock = lock
        if keys is None:
            keys = []
        self.keys = keys
        self.opened = opened

    def __hash__(self):
        return hash((self.idx, self.lock, tuple(self.keys), self.opened))

    def __cmp__(self, other):
        return cmp((self.idx, self.lock, tuple(self.keys), self.opened), (other.idx, other.lock, tuple(other.keys), other.opened))
        
    def copy(self):
        return Chest(self.idx, self.lock, self.keys, self.opened)
            
    def can_open(self, key):
        if key == self.lock and not self.opened:
            return True
        else:
            return False
            
    def open(self, key):
        if self.can_open(key):
            self.opened = True
            return True
        else:
            return False

    def close(self):
        self.opened = False

    def __repr__(self):
        if self.keys:
            return "<%d l=%d k=%s%s>" % (self.idx, self.lock, " ".join(map(str,self.keys)), " op" if self.opened else "")
        else:
            return "<%d l=%d%s>" % (self.idx, self.lock, " op" if self.opened else "")
        

cache = {}
def solve(keys, chests, no_chests, used=None, cnt=0):

    if used is None:
        used = []

        
    print cnt, "--"
    print cnt, "keys", keys
    print cnt, "chests", chests
    print cnt, "used", used
    
    if len(used) == no_chests:
        print cnt, "ret", used
#        cache[cache_key] = True
        return True
        
#    for chest in chests:
#        if not chest.opened:
#            break
#    else:
#        return used

    print cnt,"len(keys)", len(keys)
    if len(keys) == 0:
        print "no more keys!"
#        cache[cache_key] = False

        return False
    
    print cnt, "todo", [c for c in chests if c not in used]

    used_set = set(used)    
    for cidx, chest in enumerate([x for x in chests if x not in used_set]):
        print cnt, "cidx", cidx
        if chest.lock in keys:
            print cnt,"opening", chest, "with key", chest.lock
            keys_cp = keys + chest.keys
            keys_cp.remove(chest.lock)
            used.append(chest)
            retval = solve(keys_cp, chests, no_chests, used, cnt+1)
            if retval:
                return True
            else:
                used.remove(chest)
                print cnt, "used", used
                    
                
    print cnt,"no available chests"
#    cache[cache_key] = False
    return False

                

if __name__ == "__main__":
    infile = open(sys.argv[1])
    no_cases = int(infile.readline())
        
    
    for cidx in xrange(no_cases):
        no_keys, no_chests = read_ints(infile)
        
        keys = array("B", read_ints(infile))

        chests = []
        for i in xrange(no_chests):
            items = read_ints(infile)
            lock = items.pop(0)
            tmp = items.pop(0)
            chest = Chest(i+1, lock, array("B", items))
            chests.append(chest)

#        print chests
#        print "call", keys, chests
        used = []
        if cidx==7:
            continue
        
        cache = {}
        status = solve(keys, chests, no_chests, used)
        if not status:
            print "Case #%d: IMPOSSIBLE" % (cidx+1)
        else:
            print "Case #%d: %s" % (cidx+1, " ".join([str(c.idx) for c in used]))

 #       print "Case #%d: %d" % (cidx+1, sol)
