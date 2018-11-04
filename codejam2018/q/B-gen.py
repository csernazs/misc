
import random


n_cases = 100
print(n_cases)
for case in range(n_cases):
    n_values = random.randint(3, 10**5)
    print(n_values)
    values = [random.randint(0, 10**9) for x in range(n_values)]
    print(" ".join(map(str, values)))
    