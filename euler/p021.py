
import pdb


def get_divisors(n_max):
    retval = dict([(x, [1]) for x in xrange(1, n_max+1)])

    for divider in xrange(2, n_max/2+1):
        res = divider*2
        while res<=n_max:
            retval[res].append(divider)
            res += divider

    return retval


def solve(n_max):
    dd = get_divisors(n_max)

    retval = set()    
    for n, divs in dd.iteritems():
#        if n == 220:
#            pdb.set_trace()
        s = sum(divs)
        
#        print n, divs, s
        if s>1 and s<n_max+1 and s != n:
            if sum(dd[s]) == n:
                print n, s, divs
                retval.add(n)
    
    return retval
    

res = solve(10000)
print sum(res)


