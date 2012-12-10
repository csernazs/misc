
import sys

for num in xrange(1, (10**5)):
    if "0" in str(num):
        continue
        
    mul = 1
    res_s = ""
    while True:
        res = num * mul
        res_tmp = str(res)
        if "0" in res_tmp:
            break
        res_s += str(res)

        if len(res_s)>9:
            break
        elif len(res_s)<9:
            if len(res_s) != len(set(res_s)):
                break
        elif len(res_s) == 9:
            if len(res_s) == len(set(res_s)):
                print res_s, num, mul
        
        mul += 1

