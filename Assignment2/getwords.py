
def getwords(filename):
        words = [] 
	f = open(filename);  
	for line in f.readlines():
		words.append(line.split()[0].lower())
        return words 

#words = getwords("wordlist.txt"); 
#print words 
