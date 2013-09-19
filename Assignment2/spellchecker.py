from stredit import stredit2 
import sys
words = [] 

with open('words.txt') as f:
    words = f.read().splitlines()
def spellchecker(word):
        word = str(word).lower()
	minval = stredit2(word,words[0],False); 
	matchstring = words[0] ; 

	for matchword in words : 
		if(stredit2(word,matchword,False)<minval):
			minval = stredit2(word,matchword,False)
			matchstring = matchword 

	return matchstring 

print spellchecker(str(sys.argv[1]))
#print spellchecker("therom");
#print spellchecker("engish");
