

a=1
b=2
res = 2
while b<4000000:
    a, b = b, b+a
    if b%2 == 0:
        res = res + b

print res

    

