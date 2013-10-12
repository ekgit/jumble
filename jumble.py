'''
solve jumble (or cheat at letterpress)

python jumble.py input_string [dictionary]

input_string : input string to solve jumble for
  dictionary : path of wordlist (optional)
'''

from collections import defaultdict

def to_set(s):
    'convert sorted string into a set of its components (e.g. abbccc becomes [a,b,bb,c,cc,ccc])'
    d = defaultdict(int)
    for e in s:
        d[e] += 1
    r = set()
    for k,v in d.items():
        for i in range(1,v+1):
            r.add(k * i)
    return r

def to_canon(s):
    'get sorted version of the word (e.g. butter --> berttu)'
    s = list(s)
    s.sort()
    s = ''.join(s)
    return s

def set_to_canon(s):
    "given set of letters, find the sorted version of the word (e.g. set(['b', 'e', 'tt', 'r', 'u', 't']) --> berttu)"
    d = defaultdict(int)
    for elt in s:
        l = len(elt)
        if d[elt[0]] < l:
            d[elt[0]] = l
    ks = d.keys()
    ks.sort()
 
    return ''.join([(k * d[k]) for k in ks])
        

def load_words(path):
    '''load list of words into sets of letters, and map them to canonical, sorted versions of those words'''
    subsets = []
    word_table = defaultdict(set)
    for ln in open(path):
        ## clean the word
        word = ln.strip().lower()
        canon = to_canon(word)
        word_table[canon].add(word)
    for k in word_table.keys():
        subsets.append(to_set(k))
    return subsets,word_table

if __name__=='__main__':
    import sys
    PATH = "/usr/share/dict/words"
    if len(sys.argv) < 2:
        print "usage"
        print __doc__
        sys.exit()
    
    if len(sys.argv) > 2:
        PATH = sys.argv[2]

    arg = to_canon(sys.argv[1])
    arg_set = to_set(arg)

    print "sorted letters in word: %s" %  arg
    print "set of letters in word: %s" %  str(arg_set)
    print "loading dictionary"
    ss,wt = load_words(PATH)
    print "finished loading dictionary"

    ## for each set in the dictionary, check if the argument's set contains it
    matches = [set_to_canon(s) for s in ss if arg_set.issuperset(s)]
    matches.sort()

    ## for each matching set, print out all words in the dictionary that are anagrams of that match
    for m in matches:
        print ','.join([ e for e in wt[m]])
                
