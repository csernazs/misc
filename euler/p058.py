
from __future__ import division

import c_prime

def spiral():
    d1, d2, d3 = 3,5,7
    yield (d1, d2, d3)

    n = 3

    while True:
        d1 = d1 + n-1 + n - 1 + n + n
        d2 = d2 + n-1 + n + 1 + n + n
        d3 = d3 + n+1 + n + 1 + n + n

        yield (d1, d2, d3)
        n += 2


side = 3
cnt = 1
cnt_p = 0

for tr in spiral():
    cnt += 4
    sum_p = sum(map(c_prime.is_prime, tr))
    cnt_p += sum_p
    ratio = cnt_p / cnt
    if ratio<0.1:
        print side
        break
    side += 2

