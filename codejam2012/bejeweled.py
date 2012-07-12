

from collections import Counter

def replace_list(list, dict):
    retval = []
    for item in list:
        retval.append(dict.get(item, item))

    return retval
    
class Table(object):
    def __init__(self, data=None):
    
        if data:
            self.data = [x[:] for x in data]
            
        else:
            self.data = []
        
    def add_row(self, row):
        self.data.append(row)
    
    def __iter__(self):
        return iter(self.data)
    
    def __str__(self):
        retval = ["".join(row) for row in self]
        return "\n".join(retval)

    def get_jewel(self, row, col):
        return self.data[row][col]
        
    def set_jewel(self, row, col, value):
        self.data[row][col] = value
        
    def swap(self, pos1, pos2):
        j1 = self.get_jewel(*pos1)
        j2 = self.get_jewel(*pos2)
        
        self.set_jewel(pos1[0], pos1[1], j2)
        self.set_jewel(pos2[0], pos2[1], j1)

    def iterrows(self):
        return iter(self.data)
        
    def itercols(self):
        for col in zip(*self.data):
            yield col
            
    def set_row(self, row_no, row):
        self.data[row_no] = row
    
    def set_col(self, col_no, col):
        for row, colval in zip(self.data, col):
            row[col_no] = colval
            
    def step(self):
        change_row = change_col = False
        change_row_cur = change_col_cur = False
        
        t2 = Table(self.data)
        for (row_id, row), (row2_id, row2) in zip(enumerate(self.iterrows()), enumerate(t2.iterrows())):
            change_row_cur = change_col_cur = False

            counter = Counter(row)
            repl_dict = {}
            for key, value in counter.iteritems():
                print "key, value", key, value
                if value>=3:
                    repl_dict[key] = "."
                    change_row = True
                    change_row_cur = True
            
            if change_row_cur:
                print "change_row", change_row_cur
                print replace_list(row, repl_dict)
                t2.set_row(row_id, replace_list(row, repl_dict))
                print t2
                print "*"*10            
        
        for (col_id, col), (col2_id, col2) in zip(enumerate(self.itercols()), enumerate(t2.itercols())):
            counter = Counter(col)
            repl_dict = {}
            for key, value in counter.iteritems():
                if value>=3:
                    repl_dict[key] = "."
                    change_col = True
                    change_col_cur = True
            
            if change_col_cur:
                print repl_dict
                t2.set_col(col_id, replace_list(col2, repl_dict))

            
        return t2
        
f = open("bejeweled.in")

no_cases = int(f.readline())

for case_no in xrange(no_cases):
    print "\n",case_no, "="*10 
    no_rows, no_cols = map(int, f.readline().split(" "))
    print case_no, no_rows, no_cols
    table = Table()
    for row_no in xrange(no_rows):
        table.add_row(list(f.readline().strip()))

    print table
    print repr(table.data)

    table.swap([0,0],[0,1])    
    print "-"*10
    print table
    
    table.set_row(0, ["Q"]*no_cols)
    print "-"*10

    print table

    table.set_col(0, ["Q"]*no_rows)
    print "-"*10

    print table


    print "-"*10
    print table.step()
    