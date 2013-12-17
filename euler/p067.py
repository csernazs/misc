


tree = []
with open("triangle.txt") as f:
  for line in f:
    tree.append(map(int, line.strip().split()))


for rowid in xrange(len(tree)-2, -1, -1):
    row = tree[rowid]
    for colid, value in enumerate(row):
        tree[rowid][colid] = max(tree[rowid+1][colid], tree[rowid+1][colid+1]) + value

print tree[0][0]
