

def counter(symbols):
    length = len(symbols)
    indexes = [0]*length
    lengths = [len(x) for x in symbols]

    yield [symbols[idx][indexes[idx]] for idx, iidx in enumerate(indexes)]
    
    while True:
        for iidx in xrange(length-1, -1, -1):
            if indexes[iidx]<lengths[iidx]-1:  
                indexes[iidx] += 1
                break
            else:
                indexes[iidx] = 0

        else:
            break
            
        yield [symbols[idx][iidx] for idx, iidx in enumerate(indexes)]




for i in counter(["a", "def", "ghijk"]):
    print i
    
            