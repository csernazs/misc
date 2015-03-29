#!/usr/bin/pypy

import sys

def read_int(f):
    return int(f.readline())

def read_ints(f, sep=" "):
    return map(int, f.readline().rstrip().split(sep))

def read_lines(f, no_lines):
    retval = []
    for i in xrange(no_lines):
        retval.append(f.readline().rstrip())
    return retval


words = [a.rstrip() for a in open("garbled_email_dictionary.txt")]
words_set = set(words)

words_len = {}
for word in words:
    if len(word) not in words_len:
        words_len[len(word)] = [word]
    else:
        words_len[len(word)].append(word)

for key, value in words_len.iteritems():
    print key, len(value)

def solve(ctext):
#    print ctext
    if ctext in words_set:
        return 0

    if len(ctext) in words_len:
        opts = words_len[len(ctext)]

        tcnt = None
        for opt in opts:
            oidx = None
            cnt = 0

            for cidx, chr in enumerate(ctext):
                if chr != opt[cidx]:
                    if oidx is None or cidx-oidx>=5:
                        cnt += 1
                        oidx = cidx
                    else:
                        break
            else:
                if tcnt is None or cnt<tcnt:
                    tcnt = cnt

        if tcnt is None:
            result = None
            for left, right in [(ctext[:i], ctext[i:]) for i in xrange(1, len(ctext))]:
                tresult = solve(left) + solve(right)
                if result is None or tresult<result:
                    result = tresult
            
            return result
                    
                                    
        return tcnt


def diff(text1, text2, maxdiff=None, offset=-1):
    retval = []
    oidx = None
    for idx, pair in enumerate(zip(text1, text2)):
        if pair[0] != pair[1]:
            if idx<offset:
                return None
            if maxdiff is not None and len(retval)==maxdiff:
                return None
            if oidx is not None and idx-oidx<5:
                return None
            else:
                oidx = idx

            retval.append(idx)

    return tuple(retval)
    
def solve(ctext, offset=-1):
    indexes_len_min = None
    potential = []
    for length in xrange(min(7, len(ctext)), 1, -1):
        tmp = ctext[:length]
        print "tmp", tmp
        for word in words_len[length]:
            indexes = diff(word, tmp, 2, offset)
            if indexes is not None:
                potential.append((len(indexes), word, indexes))

    potential.sort()
    for idx_len, word, indexes in potential:
        if len(indexes) == 0:
            off = -1
        else:
            off = 5 - len(word) - 1 - indexes[-1]
            if off <0:
                off = -1
        solve(ctext[len(word):], off)
        
    
        
    
    

if __name__ == "__main__":
    infile = open(sys.argv[1])
    no_cases = int(infile.readline())
    
    
    for cidx in xrange(no_cases):
        ctext = infile.readline().rstrip()
        sol = solve(ctext)
        print "Case #%d: %s" % (cidx+1, sol)
