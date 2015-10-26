

def f(k):
    return (k * (3 * k - 1)) / 2

def g():
    i = 1
    while True:
        yield i
        yield 0-i
        i=i+1
        
cache = {0: 1, 1: 1, 2:2, 3:3, 4:5, 5:7, 6:11}

def p(n):
    # print n
    if n<0:
        return 0

    if n in cache:
        return cache[n]
    else:
        result = 0
        k = 1
        for k in g():
            # print "k", k
            # print "n", f(k)
            part = (-1)**(k-1) * p(n-(k*(3*k-1)/2))
            if part == 0:
                break
            else:
                result += part
                k += 1

        cache[n] = result
        return result

print int(p(100)-1)
    