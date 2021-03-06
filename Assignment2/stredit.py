import sys
def find_min_in_table(table) :
	mini= 0 ; 
        minj= 0 ;
        minval = table[mini][minj];  
        for i in range(0,len(table)):
	   for j in range(0,len(table[0])): 
		 if table[i][j]<minval:
                     minval = table[i][j]; 
		     mini = i ; 
		     minj  = j; 

        return (mini,minj) 

def print_table(s1,s2,table,trace=None):
    """print the DP table, t, for strings s1 and s2.  
    If the optional 'trace' is present, print * indicators for the alignment.
    Fancy formatting ensures this will also work when s1 and s2 are lists of strings"""
    print "       ",
    for i in range(len(s1)):
        print "%3.3s" % s1[i],
    print
    for i in range(len(table)):
        if i > 0: print "%3.3s" % s2[i-1], 
        else: print '   ',
        for j in range(len(table[i])):
            if trace and trace[i][j] == "*":
                print "*" + "%2d" % table[i][j],
            else:
                print "%3d" % table[i][j],
        print

def argmin (*a):
    """Return two arguments: first the smallest value, second its offset"""
    min = sys.maxint; arg = -1; i = 0
    for x in a:
        if (x < min):
            min = x; arg = i
        i += 1
    return (min,arg)
            

def stredit (s1,s2, showtable=True):
    "Calculate Levenstein edit distance for strings s1 and s2."
    len1 = len(s1) # vertically
    len2 = len(s2) # horizontally
    # Allocate the table
    table = [None]*(len2+1)
    for i in range(len2+1): table[i] = [0]*(len1+1)
    # Initialize the table
    for i in range(1, len2+1): table[i][0] = i
    for i in range(1, len1+1): table[0][i] = i
    # Do dynamic programming
    for i in range(1,len2+1):
        for j in range(1,len1+1):
            if s1[j-1] == s2[i-1]:
                d = 0
            else:
                d = 1
            table[i][j] = min(table[i-1][j-1] + d,
                              table[i-1][j]+1,
                              table[i][j-1]+1)
    if showtable:
        print_table(s1, s2, table)
    return table[len2][len1]

def stredit2 (s1,s2, showtable=True):
    "Implementing the Smith Waterman Distance " 
    "String edit distance, keeping trace of best alignment"

    " Assigning costs for each operation " ; 
    ins_del_cost = 1  
    copy_cost = -2
    subs_cost = 1
    base_cost = 0 

    len1 = len(s1) # vertically
    len2 = len(s2) # horizontally
    # Allocate tables
    table = [None]*(len2+1)
    for i in range(len2+1): table[i] = [0]*(len1+1)
    trace = [None]*(len2+1)
    for i in range(len2+1): trace[i] = [None]*(len1+1)
    # initialize table
    for i in range(1, len2+1): table[i][0] = i
    for i in range(1, len1+1): table[0][i] = i
    # in the trace table,1=subst, 2=insert, 3=delete
    for i in range(1,len2+1): trace[i][0] = 1
    for j in range(1,len1+1): trace[0][j] = 2
    # Do dynamic programming
    for i in range(1,len2+1):
        for j in range(1,len1+1):
            if s1[j-1] == s2[i-1]:
                d = copy_cost 
            else:
                d = subs_cost 
            # if true, the integer value of the first clause in the "or" is 1
            table[i][j],trace[i][j] = argmin(0, 
  					     table[i-1][j-1] + d,
                                             table[i-1][j]+ins_del_cost,
                                             table[i][j-1]+ins_del_cost)

    (mini,minj) = find_min_in_table(table) 
    
    if showtable:
	# If you are implementing Smith-Waterman, then instead of initializing
	# i=len2 and j=len1, you must initialize i and j to the indices 
	# of the table entry that has the miminum value (it will be negative)
        "This finds the end point " 
        i = mini 
	j = minj 
        while (i>0 and j>0) and (i!=0 or j!=0):

	    if trace[i][j] == 1:
                nexti = i-1
                nextj = j-1
            elif trace[i][j] == 2:
                nexti = i-1
                nextj = j
            elif trace[i][j] == 3:
                nexti = i
                nextj = j-1
	    else:
		nexti = 0
		nextj = 0
            trace[i][j] = "*"
            i = nexti
            j = nextj
	    print "ij", i, j,
            if trace[i][j] == 1 :
                print "copy/sustitute"
            elif trace[i][j] == 2:
                print "insert"
            elif trace[i][j] ==3:
                print "delete"
            else :
                print "base:0"

	print     
        print_table(s1, s2, table, trace)
    return table[mini][minj]


#stredit2('mccallum', 'mcalllomo')
#stredit(['this', 'is', 'a', 'test'], ['this', 'will', 'be', 'another', 'test'])
#print stredit2("s'allonger", "lounge")
#print stredit2("William W. Cohen","William W. 'Dont call me that' Cohen") 
#print stredit2("lounge", "s'allonger")
#print stredit2('cow over the moon', 'moon in the sky')
#print stredit2('another fine day', 'anyone can dive')
#print stredit2('another fine day in the park', 'anyone can see him pick the ball')

# import dicts
# argvlen = len(sys.argv)
# target = sys.argv[argvlen-2].lower()
# filename = sys.argv[argvlen-1]
# d = dicts.DefaultDict(0)
# for word in open(filename).read().split():
#     if word not in d:
#       word = word.lower()
#       d[word] = stredit(word, target, False)
# print d.sorted(rev=False)[:20]

