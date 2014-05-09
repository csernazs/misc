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


class Node(object):
    def __init__(self, number, edges=None):
        self.number = number
        if not edges:
            self.edges = set()
        else:
            self.edges = edges
    
    def __hash__(self):
        return hash(self.number)
    
    def __cmp__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return cmp(self.number, other.number)
        
    def __repr__(self):
        return "<Node %d edges %s>" % (self.number, " ".join(map(str, sorted([x.number for x in self.edges]))))

class Tree(dict):
    def add_node(self, node_num):
        if node_num not in self:
            node = Node(node_num)
            self[node_num] = node
            return node
        else:
            return self[node_num]
        
    def add_edge(self, node1, node2):
        node1 = self.add_node(node1)
        node2 = self.add_node(node2)
        node1.edges.add(node2)
        node2.edges.add(node1)
    

def is_full(root):
    visited = set([root])
    queue = [x for x in root.edges]
    retval = []
    while len(queue)>0:
        node = queue.pop(0)
        if len(node.edges) == 1: # and list(node.edges)[0] in visited:
            continue

        visited.add(node)
        if len(node.edges) == 3:
            for subnode in node.edges:
                if subnode in visited:
                    continue
                else:
                    queue.append(subnode)
        else:
            retval.append(node)
            
            
    return retval

cache = {}
def get_children(node):
    if node in cache:
        return cache[node]

    queue = [node]
    visited = set([node])
    retval = []
    while len(queue)>0:
        node = queue.pop(0)
        retval.append(node)
        visited.add(node)
        for subnode in node.edges:
            if subnode not in visited:
                queue.append(subnode)
    retval = retval[1:]
    cache[node] = retval
    return retval
    
def solve(tree):
    for node in tree.itervalues():
        if len(node.edges) == 2:
            print "possible root", node
            to_delete = is_full(node)
            print "to_delete", to_delete
            no_deletes = 0
            for node_delete in to_delete:
                children = get_children(node_delete)
                no_deletes += len(children)+1
                
            print "no_deletes", no_deletes
        
def main():
    global cache
    f = open(infile, "r")
    no_cases = read_int(f)

    for case_idx in xrange(no_cases):
        print "=== CASE", case_idx+1
        cache = {}
        tree = Tree()
        no_nodes = read_int(f)
        for edge_idx in xrange(no_nodes-1):
            edge = read_ints(f)
            tree.add_edge(edge[0], edge[1])
        
        print tree
        solve(tree)
        
#        sol = solve(i)
#        out.write("Case #%d: %s %s\n" % (case_idx+1, sol))
        

if __name__ == "__main__":
    main()
    
