
cache = {}
def get_series(n):
    if cache.get(n):
        return cache[n]
    else:
        retval = [n]

    curr = n
    
    while curr!=1:
        if cache.get(curr):
#            print "cache hit %d" % curr
            retval.extend(cache[curr])
            cache[n] = retval
            return retval
        
        if curr%2 == 0: # even
            curr = curr / 2
        else:
            curr = 3 * curr + 1
        
        retval.append(curr)
    
    for idx, x in enumerate(retval):
        cache[x] = retval[idx:]
    return retval
    

max_len = 0
for start in xrange(13, 1000000, 2):
    curr_len = len(get_series(start))
    if curr_len>max_len:
        sol = start
        max_len = curr_len

print sol, curr_len

print get_series(sol)

    
#print get_series(16)
    
#print get_series(113)
    
    

    