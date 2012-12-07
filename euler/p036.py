


cnt = 0
for num in xrange(1,10**6):
    num_s = str(num)
    num_r = num_s[::-1]
    
    if num_s == num_r:
        num_bin = bin(num)[2:]
        num_bin_r = num_bin[::-1]
        if num_bin == num_bin_r:
            print num_s, num_bin
            cnt += num
            
print "--"
print cnt
            
