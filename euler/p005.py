

def solve(n):
    dividers = []
    for i in xrange(2,n):
        if n%i != 0:
            dividers.append(i)
            
    
    dividers.reverse()

    p = n
    while True:
        
        for d in dividers:
            if p%d != 0:
                break
        else:
            return p
        
        p = p + n
    
    
    
n=20
result = solve(n)
print result
print

for i in xrange(2, n+1):
    div, mod = divmod(result, i)
    if mod != 0:
        print "error"
        
    print "%d/%d = %d" % (result, i, div)
    
