

data =  open("names.txt").read().replace('"', "").split(",")

data.sort()

result = 0
for idx, name in enumerate(data):
    value = sum([ord(x)-64 for x in name])
    result += value * (idx+1)
    
print result

    