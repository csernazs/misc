
import math

f = open("quake.txt")
no_cases = int(f.readline().strip())


for case_no in xrange(no_cases):
    case = f.readline().strip()
    fields = case.split(" ")
    no_players, skills = (int(fields[0]), map(int, fields[1:]))
    

    skills.sort()

    orig_skills = skills
    h = 4
    
    sol = []
    for i in xrange(len(skills)):
        skills = orig_skills[:]
        for j in xrange(len(skills)):
            diff = abs(sum(skills[:h]) - sum(skills[h:]))
#            print diff
            skills[i], skills[j] = skills[j], skills[i]
            sol.append(diff)
            
    print "Case #%d: %d" % (case_no+1,  min(sol))
                

f.close()
    