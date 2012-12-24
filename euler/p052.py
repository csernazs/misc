

n = 1
while True:
    n_s = str(n)
    n_map = {a: n_s.count(a) for a in n_s}
    
    for mul in (6,5,4,3,2):
        res = n*mul
        res_s = str(res)
        
        if len(res_s) == len(n_s):
            res_map = {a: res_s.count(a) for a in res_s}
            if res_map != n_map:
                break
        else:
            break
    else:
        print "sol", n_s
        for mul in (6,5,4,3,2):
            print n*mul
        break
        

    n+= 1
    
