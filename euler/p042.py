
from math import sqrt

cnt = 0
for qword in open("words.txt").read().split(","):
    word = qword[1:-1]
    x = sum([ord(x)-64 for x in word])
    
    n = -0.5 + sqrt(0.25 + 2*x) 
    if n == int(n):
        cnt += 1
        print word

print cnt    
    
    