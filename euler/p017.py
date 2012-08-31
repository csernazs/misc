


ones = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]

tens = [None, None, "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]

hundred = "hundred"

def get_number_as_string(n):
    if n<=20:
        return ones[n]
    
    if 20<n<100:
        retval = tens[n/10]
        rem = n%10
        if rem:
            retval += "-" + ones[rem]
            
        return retval

    if n >= 100 and n<1000:
        rem = n%100
        retval = ones[n/100]+" hundred"
        
        if rem:
            retval += " and "+get_number_as_string(rem)
            
        return retval
    
    if n >= 1000:
        rem = n%1000
        retval = ones[n/1000]+" thousand"
        
        if rem:
            retval += " and "+get_number_as_string(rem)
            
        return retval
                    
        
        


def get_len(n):
    text = get_number_as_string(n)
    length = len(text.replace(" ", "").replace("-", ""))
    return length

print sum([get_len(n) for n in xrange(1, 1001)])
