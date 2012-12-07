
from itertools import permutations

full_set = set(map(str, range(1, 10)))

def solve(left_length, right_length):
    for left_digits in permutations(map(str, range(1, 10)), left_length):
        right_set = full_set - set(left_digits)
        for right_digits in permutations(right_set, right_length):
            left_s = "".join(left_digits)
            right_s = "".join(right_digits)
            prod = int(left_s)*int(right_s)
            prod_s = str(prod)
            if "0" not in prod_s and len(set(prod_s+left_s+right_s)) == len(prod_s)+left_length+right_length:
                yield (left_s, right_s, prod)
            
prods = set()

for left_length, right_length in [(3, 2), (1, 4)]:
    for left, right, prod in solve(left_length, right_length):
        print left, right, prod
        prods.add(prod)

print sum(prods)
