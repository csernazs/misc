

class Node(object):
    def __init__(self, name, parent=None, children=None):
        self.name = name
        self.parent = parent
        
        if not children:
            children = []
        self.children = children
        
    def __repr__(self):
        if self.parent:
            return "<Node name=%r parent=%r children=%r>" % (self.name, self.parent.name, [x.name for x in self.children])
        else:
            return "<Node name=%r parent=%r, children=%r>" % (self.name, self.parent, [x.name for x in self.children])

class Tree(object):
    def __init__(self):
        self.nodes = {}

    
    def create_node(self, name):
        if name not in self.nodes:
            node = Node(name)
            self.nodes[name] = node
            return node
        else:
            return self.nodes[name]
            
    def create_node_parent(self, name, parent):
        node = self.create_node(name)
        parent_node = self.create_node(parent)
        node.parent = parent_node
        parent_node.children.append(node)
        
            
            
        
f = open("tech.txt")

no_cases = int(f.readline())
for case_id in xrange(no_cases):
    techs = []
    no_technologies = int(f.readline())
    for tech_id in xrange(no_technologies):
        techs.append(f.readline().strip().split(":"))
        

    dsts = []
    no_dsts = int(f.readline())
    for dst_id in xrange(no_dsts):
        dsts.append(f.readline().strip())
        

    tree = Tree()
        
    for tech1, tech2 in techs:
        tree.create_node_parent(tech2, tech1)

    sol = []
        
    for dst in dsts:
        
        try:
            nodes = [tree.nodes[dst]]
        except KeyError:
            sol.append(dst)
            continue

        def print_tree(nodes, retval):
            if not nodes:
                return
                                
            for node in nodes:
                print_tree(node.children, retval)
                retval.append(node)

        print_tree(nodes, sol)
    
    seen = set()    
    sols_f = []
    for s in sol:
            
        if s not in seen:
            seen.add(s)
            if type(s) == str:
                sols_f.append(s)
            else:
                sols_f.append(s.name)
        
    print "Case #%d: %d" % (case_id+1, len(sols_f))
    
    for sol_f in sols_f:
        print sol_f
                    