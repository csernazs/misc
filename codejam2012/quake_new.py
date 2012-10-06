
from itertools import combinations


f = open("quake.txt")
 
no_cases = int(f.readline().strip())

def solve(skills):
    total = sum(skills)


    old_diff = 10e400
    
    for left in combinations(skills, len(skills)/2):
        left_sum = sum(left)
        right_sum = total - left_sum
        diff = abs(left_sum-right_sum)
        if diff == 0:
            return diff
            
        if diff < old_diff:
            old_diff = diff
            

    return old_diff


for case_no in xrange(no_cases):
    case = f.readline().strip()
    fields = case.split(" ")
    no_players, skills = (int(fields[0]), map(int, fields[1:]))
    

        
    sol = solve(skills)
    
    print "Case #%d: %d" % (case_no+1,  sol)
    
    



f.close()
