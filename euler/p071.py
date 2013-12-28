


n = 2
d = 5

cnt = 2
MAX = 1000000
while d<MAX:
    n = n + 3
    d = d + 7
    cnt += 1

print "%d/%d" % (n-3, d-7)
