

from datetime import date
from monthdelta import MonthDelta as monthdelta

start = date(1901, 1, 1)

end = date(2000, 12, 31)

curr = start

cnt = 0

while curr < end:
    print curr
    curr = curr + monthdelta(1)
    if curr.isoweekday() == 7:
        cnt += 1
    
print cnt
