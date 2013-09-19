
def getwords(filename):
        words = []
        f = open(filename);
        for line in f.readlines():
                words.append(line.split()[0].lower())
        return words
	f.close(); 

words = getwords("wordlist.txt") ;

thefile = open("words.txt","w")
for item in words:
  thefile.write("%s\n" % item)

thefile.close()
