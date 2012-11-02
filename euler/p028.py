

numbers = [1]
n = 1
step = 2
cnt = 0

while len(numbers)<(1001*2-1):
    n = n + step
    cnt = cnt + 1
    numbers.append(n)
    if cnt>3:
        cnt = 0
        step = step + 2

#print numbers        
print len(numbers)
print sum(numbers)
    