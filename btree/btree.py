#!/usr/bin/env python


import collections

class Node(object):
    def __init__(self):
        self.children = []
        self.items = []
    
    def add(self, key, value, maxsize):
        print "add", key, value, maxsize
        print "items", self.items
        
        if len(self.items) == 0:
            self.items.append((key, value))
            self.children = [None, None]
    
        elif len(self.items) == 1:
            if key > self.items[0][0]:
                self.items.append((key, value))
                self.children.append(None)
            else:
                self.items.insert(0, (key, value))
                self.children.insert(0, None)

        elif len(self.items) < maxsize:
            if key < self.items[0][0]:
                self.items.insert(0, (key, value))
                self.children.insert(0, None)
            else:
                for idx in xrange(len(self.items)-1):
                    left = self.items[idx]
                    right = self.items[idx+1]
#                    print "left", left
#                    print "right", right
                    if key >= left[0] and key < right[0]:
                        self.items.insert(idx+1, (key, value))
                        self.children.insert(idx+1, None)
                        break
                else:
                    assert key >= right[0]
                    self.items.append((key, value))
                    self.children.append(None)
        
        elif len(self.items) >= maxsize:
            if key < self.items[0][0]:
                child_node = self.children[0]
                child_idx = 0
            else:
                for idx in xrange(len(self.items)-1):
                    left = self.items[idx]
                    right = self.items[idx+1]
#                    print "left", left
#                    print "right", right
                    if key >= left[0] and key < right[0]:
                        child_node = self.children[idx+1]
                        child_idx = idx+1
                        break
                else:
                    assert key >= right[0]
                    child_node = self.children[-1]
                    child_idx = len(self.children)-1
            
            
            print "found children", child_node, child_idx
            
            if child_node is None:
                child_node = Node()
                self.children[child_idx] = child_node

            child_node.add(key, value, maxsize)


    def find(self, key):
        if len(self.items) == 0:
            raise KeyError, "No such key: %s" % key

        elif len(self.items) == 1:
            if key == self.items[0][0]:
                return self.items[0][1]
            elif key < self.items[0][0]:
                child_node = self.children[0]
            else:
                child_node = self.children[1]
            
            if child_node:
                return child_node.find(key)
            else:
                raise KeyError, "No such key: %s" % key
                
                        
        if key < self.items[0][0]:
            child_node = self.children[0]

            if child_node:
                return child_node.find(key)
            else:
                raise KeyError, "No such key: %s" % key

            
        for idx in xrange(len(self.items)-1):
            left = self.items[idx]
            right = self.items[idx+1]
            
            if key == left[0]:
                return left[1]
            elif key == right[0]:
                return right[1]
            elif key > left[0] and key < right[0]:
                child_node = self.children[idx+1]
                if child_node is None:
                    raise KeyError, "No such key: %s" % key
                else:
                    return child_node.find(key)
        
        assert key > right[0]
        child_node = self.children[-1]
        if child_node is not None:
            return child_node.find(key)
        else:
            raise KeyError, "No such key: %s" % key
            
                
        
    def __repr__(self):
        return "<Node items='%s'>" % " ".join(map(str, [x[0] for x in self.items]))

def printnode(node, indent=0):
    print " "*indent*4 + repr(node)
    if node is None:
        return
        
    for child in node.children:
        printnode(child, indent+1)
    

class BTree(object):
    def __init__(self, maxsize):
        self.root = Node()
        self.maxsize = maxsize
    
    def add(self, key, value):
        self.root.add(key, value, self.maxsize)
        
    def __setitem__(self, key, value):
        self.add(key, value)

    def find(self, key):
        return self.root.find(key)
        
    def __getitem__(self, key):
        return self.find(key)

    def __repr__(self):
        return repr(self.root)
        
            
d = collections.OrderedDict()
d[3] = "a"
d[5] = "b"
d[4] = "c"
d[1] = "d"
d[10] = "e"
d[2] = "f"
d[100] = "g"
d[20] = "h"
d[50] = "i"
d[30] = "j"
d[130] = "k"

bt = BTree(3)

for key, value in d.iteritems():
    bt[key] = value

print "-"*10
printnode(bt.root)



print bt[50]
print bt[130]
print bt[3]
print 1
print bt[1]

for key, value in d.iteritems():
    assert bt[key] == value
                    