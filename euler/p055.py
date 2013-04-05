

def is_lychrel(num):
    #print "=== %d" % num
    for trial in xrange(50):
        num_s = str(num)
        num_rev = int("".join(num_s[::-1]))
        #print num_s, num_rev
        
        if num == num_rev and trial>0:
            return False
        
        num = num + num_rev
    
    return True
        
cnt = 0

for num in xrange(10, 10000):
    if is_lychrel(num):
        cnt += 1
        #print "L", num
        
print cnt
