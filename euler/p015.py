

from itertools import permutations

cnt = 0
# 2x2
for a in "DR":
    for b in "DR":

        if a == "D" and b == "D":
            cnt += 1
        elif a == "R" and b == "R":
            cnt += 1
        elif a == "R" and b == "D":
            cnt += 2
        elif a == "D" and b == "R":
            cnt += 2    
        

print cnt

cnt = 0
# 2x2
for a in "DR":
    for b in "DR":
        for c in "DR":
            for d in "DR":
            
        if a == "D" and b == "D":
            cnt += 1
        elif a == "R" and b == "R":
            cnt += 1
        elif a == "R" and b == "D":
            cnt += 2
        elif a == "D" and b == "R":
            cnt += 2    
            
            
#print len(set(permutations("DDRR")))

#print len(set(permutations("D"*10+"R"*10)))
