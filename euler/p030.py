
sol = 0

exp = 5
str_to_int = {str(i): i**exp for i in xrange(10)}

for num in xrange(2, 1000000):
    digits_sum = 0

    for digit_s in str(num):
        digit_exp = str_to_int[digit_s]
        digits_sum += digit_exp
        if digits_sum > num:
            break
    
    if digits_sum == num:
        print num
        sol += num            
        
print ">"*3
print sol

    
    
    