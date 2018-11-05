

text = open("input1.txt", "r").read().strip()

result = 0
for idx, c in enumerate(text):
    try:
        if text[idx+1] == c:
            result += int(c)
    except IndexError:
        if text[0] == c:
            result += int(c)
            

print(result)

