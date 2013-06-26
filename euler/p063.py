

def get_numbers(n):
    a = 1
    
    min = 10**(n-1)
    max = 10**n
    
    while True:
        t = a**n
        if t>=min and t<max:
            yield t
        if t>max:
            break
        a+=1

i = 1
cnt = 0
while True:
    q = True
    for n in get_numbers(i):
        print n
        q = False
        cnt += 1
        
    if q:
        break
    i += 1
    
print cnt

    