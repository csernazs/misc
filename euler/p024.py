

from itertools import permutations, islice

for i in islice(permutations("0123456789", 10), 999999, 1000000):
    print "".join(map(str, i))
