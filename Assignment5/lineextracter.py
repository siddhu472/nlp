f = open("wsj15-18.pos")
f1 = open("trainingFile","w")
f2 = open("testFile","w") 

linecount = 0 ; 
trainlines = [] 
testlines = []  
for lines in f.xreadlines():
	linecount = linecount + 1 
	if linecount < 200 : 
		f2.write(lines) 
	else : 
		f1.write(lines)
	 
print linecount 
f.close()
f1.close()
f2.close()


		
