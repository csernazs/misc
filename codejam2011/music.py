#!/usr/bin/python -u
import sys
import collections
import multiprocessing
import os

def read_file(file):
    state = 0
    songs = []
    for l in file:
        line=l.strip()
        if state == 0:
            no_cases = int(line)
            cnt = 0
            state = 1
        elif state == 1:
            no_songs = int(line)
            state = 2
        elif state == 2:
            songs.append(line.upper())
            no_songs -= 1
            if no_songs == 0:
                yield songs
                songs = []
                state = 1
                

def get_substrings(str, length):
    return [str[i:i+length] for i in xrange(0, len(str)-(length-1))]

def find_song(songs, key):
    found = False
    ret = None
    for song in songs:
        if key in song:
            if found == False:
                ret = song
                found = True
            else:
                raise ValueError, "Duplicate match %r %r %r" % (ret, key, song)
    return ret
    
            
def solve(songs, length, solved=None):
    if length>max(map(len, songs)):
        return solved
    #print "length:",length
    if not solved:
        solved = []
        solved_set = set()
    else:
        solved_set = set(solved)
        
    sets = []
    song_sets = []
    union = set()
    for song in songs:
        new_set = set(get_substrings(song, length))
        #print "new_set:", song, new_set
        song_sets.append(new_set)
        union = union.union(new_set)

    for song_set1_idx in xrange(len(song_sets)-1):
        for song_set2_idx in xrange(song_set1_idx+1, len(song_sets)):
            diff = song_sets[song_set1_idx].intersection(song_sets[song_set2_idx])
            #print diff
            union = union - diff

    for token in sorted(union):
        #print "TOK: %r" % token
        song = find_song(songs, token)
        if song not in solved_set:
            solved_set.add(song)
            solved.append((token,song))
    
    #print solved
    solved = reduce_solved_list(solved)
    if len(solved) < len(songs):
        return solve(songs, length+1, solved)
    else:
#        print "len(solved), len(songs)", len(solved), len(songs)
#        print solved
        return solved
        

def reduce_solved_list(solved):
    ret = []
    for key, value in reduce_solved(solved).iteritems():
        ret.append((value, key))
    return ret
    
def reduce_solved(solved):
    ret =  {}
    for key, value in solved:
        if  value not in ret:
            ret[value] = key
    return ret

def solve_case(songs):
#    print "SOLVE_CASE pid=%d length=%d" % (os.getpid(), len(songs))
    retval = []
    if len(songs) <2:
        retval.append("")
    else:
        solved = solve(songs, 1)
        solved_dict = reduce_solved(solved)
        for song in songs:
            if song in solved_dict:
                retval.append(solved_dict[song])
            else:
                retval.append(None)
    
    return retval
    
def main():
    songs_list = read_file(sys.stdin)
    pool = multiprocessing.Pool(2)
    results = pool.map(solve_case, songs_list)
    pool.close()
    for idx, results in enumerate(results):
        print "Case #%d:" % (idx+1)
        for result in results:
            if result == None:
                print ":("
            else:
                print '"%s"' % result
        
if __name__ == "__main__":
    main()