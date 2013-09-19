import sys

 
def argmax (*a):
    """Return two arguments: first the largest value, second its offset"""
    max = -sys.maxint; arg = -1; i = 0
    for x in a:
        if (x > max):
            max = x; arg = i
        i += 1
    return (max,arg)

def print_table(s1,s2,table,trace): 
    """print the DP table, t, for strings s1 and s2.  
    If the optional 'trace' is present, print  indicators S/X/Y for the alignment.
    Fancy formatting ensures this will also work when s1 and s2 are lists of strings
    S - Substitution 
    X - X gap 
    Y - Y gap"""

    print "       ",
    for i in range(len(s1)):
        print "%5.5s" % s1[i],
    print
    for i in range(len(table)):
        if i > 0: print "%5.5s" % s2[i-1], 
        else: print '     ',
        for j in range(len(table[i])):
            if trace and trace[i][j] != 0:
                print trace[i][j] + "%4d" % table[i][j],
            else:
                print "%5d" % table[i][j],
        print

# This function is unused , used it for debugging 
def print_table_3d(s1,s2,table):
    '''In Affine gap since we have to consider the x gaps/y gaps/and match , we need 3 elements in each index of the table'''
    print "%32s"%"",
    for i in range(len(s1)):
        print "%16s" % s1[i],
    print
    for i in range(len(table)):
        if i > 0: print "%16s" % s2[i-1],
        else: print "%16s" %"0",               
        for j in range(len(table[i])):
                for k in range(0,3):
                    if (table[i][j][k] <= -100):
			print "%5s" % "-inf", 
		    else:  
			print "%5s" % str(table[i][j][k]),
                # Separator to show the three values 
		print "|",
        print

def stredit3(word,matchword):
        
	len1 = len(matchword)+1 
        len2 = len(word)+1 
        neginfinity = -100
	table = [0]*len1 # 3D table for building the Insertionx , Insertiony and copying matrices 
	trace = [0]*len1  
        A = -3 
        B = -1 

        #Allocate the table  
        for i in range(0,len(table)): 
        	table[i] = [0]*len2
        	trace[i] = [0]*len2
	for i in range(0,len(table)):
		for j in range(0,len(table[i])):
			if i==0 or j==0:
				table[i][j] = [neginfinity]*3;
			else:
				table[i][j] = [0]*3 
			trace[i][j] = [0]*3 

	#Initialize the table 
        for i in range(0,len(table)): 
		for j in range(0,len(table[i])):
			if i==0 and j==0 :
				table[0][0][0]= 0 
			if j==0 :
				table[i][0][1]= A + B*i 
			if i==0 :
				table[0][j][2] = A+ B*j 
	
	 
        #Do Dynamic Programming 
	# Here the cost of copying is 1 and the insertion of gaps is -1 
	for i in range(1,len1):
        	for j in range(1,len2):
            		if word[j-1] == matchword[i-1]:
  				d = 1
            		else:
                		d = -1
			# 0 is copy /1 insert gap in x /2 insert gap in y 
			table[i][j][0],trace[i][j][0] = argmax(table[i-1][j-1][0] + d,
                              	table[i-1][j-1][1]+d,
                              	table[i-1][j-1][2]+d)
			# 0 is open gap /1 is extend gap in x 
	    		table[i][j][1],trace[i][j][1] = argmax(table[i-1][j][0]+A+B,table[i-1][j][1]+B)
			# 0 is open gap / 1 is extend gap in y 
            		table[i][j][2],trace[i][j][1] = argmax(table[i][j-1][0]+A+B,table[i][j-1][2] +B) 
	#print_table_3d(word,matchword,table)
	#print_table_3d(word,matchword,trace)

	#Creating a representation likes the ones for the other string distances 
	final_table = [0]*len1 
	final_trace = [0]*len1
	for i in range(0,len(final_table)):
		final_table[i] = [0]*len2
		final_trace[i] = [0]*len2  
		 
	for i in range (0,len(table)):
		for j in range(0,len(table[i])):
			final_table[i][j] = max(table[i][j])		
	
	i = len1-1 
	j = len2-1 
	word1 = [] 
	word2 = [] 
	while i>=0 and j>=0 :	
		k = table[i][j].index(max(table[i][j]))
		if k ==  0: 
	     		nexti = i-1 
	     		nextj = j-1
			final_trace[i][j] ="S" 
			trace[i][j][k]="S"
			if i>0 and j>0 : 
				word1.append(word[j-1])
				word2.append(matchword[i-1])
			#print i,j,trace[i][j][k]
		if k == 1:
			nexti = i-1 
			nextj = j 
			if i>0 :
				word1.append("_")
				word2.append(matchword[i-1])
			final_trace[i][j] ="X"
			trace[i][j][k]="X"
			#print i,j,trace[i][j][k]
		if k == 2 :
			nexti = i
			nextj = j-1
			final_trace[i][j]="Y"
			trace[i][j][k]="Y"
			if j>0:
				word1.append(word[j-1])
				word2.append("_")
			#print i,j,trace[i][j][k]
		i=nexti
		j=nextj 

	
	print_table(word,matchword,final_table,final_trace)
	print "%15s"%"String: "+" ".join(word1)[::-1]
	print "%15s"%"match string: "+" ".join(word2)[::-1]  
			 

stredit3("aystqrcdef","axrstcye'f")
#stredit3("William W. Cohen","William W. 'something'  Cohen")       
#stredit3("siddharth chidambaram","siddharth axyz chidambaram") 
#stredit3("hello","hi")
#stredit3("abcd","efghi")
#stredit3("hi","hello")
