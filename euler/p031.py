

import math
from itertools import *
from pprint import pprint



coins = [1, 2, 5, 10, 20, 50, 100, 200]

coins_max = coins.pop(-1)
print coins

mult = [0]*len(coins)
maximums = [coins_max/i for i in coins]


coins_len = len(coins)
coins_len_range = range(coins_len)

def calc_sum(mult):
    res = sum([coins[i] * mult[i] for i in coins_len_range])
    return res
    
def inc(mult):
    
    idx = len(mult)-1

    while True:    
        mult[idx] += 1
        if mult[idx]>maximums[idx] or calc_sum(mult)>200:
            mult[idx] = 0
            idx = idx -1
            if idx<0:
                raise OverflowError
        else:
            break


length = 1
while True:
    try:
        inc(mult)
    except OverflowError:
        break
        
    if calc_sum(mult) == 200:
        if mult[0] >190:
            print mult
        length += 1
#        print mult
    
print length
