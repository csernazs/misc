
from itertools import *

src = map(int, open("cipher1.txt").read().strip().split(","))


for key in product(range(97, 123), repeat=3):
#    print key
    plaintext = []
    for c1, c2 in izip(cycle(key), src):
        pc = c2 ^ c1
        if pc<32 or pc>122:
        ###not (pc==32 or (pc>64 and pc<91) or (pc>96 and pc<123)):
            break
            
        plaintext.append(pc)
    else:        
        print key, sum(plaintext), "".join(map(chr, plaintext))
    
    
    
    
