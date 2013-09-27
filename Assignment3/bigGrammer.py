import sys 
from random import choice

def Dict(**args): 
    """Return a dictionary with argument names as the keys, 
    and argument values as the key values"""
    return args

# The grammar
# A line like:
#    NP = [['Det', 'N'], ['N'], ['N', 'PP'], 
# means
#    NP -> Det N
#    NP -> N
#    NP -> N PP
grammar = Dict(
        Q = [['AUX','NP','VP']],
        I = [['V','NP'],['V','PP']],# An imperative begins with a verb phrase and has no subject  
	S = [['NP','VP']],
        NP = [['Det', 'N'], ['N', 'PP'],['Det','JP']],
        VP = [['V', 'NP'],['V','CNP'], ['V', 'PP']],
	PP = [['P', 'N'],['P','JP']],
        Det = ['the', 'a'],
	P = ['with'],
	JP = [['J','N']],# Adding adjectives 
	J = ['red', 'big'],
        N = ['red', 'dog', 'dogs', 'pickles', 'ball', 'light'],
        V = ['pickles', 'see', 'sees', 'liked', 'light', 'slept'],         
	AUX = [ 'Do','Does','Can'] #Adding yes no questions 
      )

def generate(phrase):
    "Generate a random sentence or phrase"
    if isinstance(phrase, list): 
        return mappend(generate, phrase)
    elif phrase in grammar:
        return generate(choice(grammar[phrase]))
    else: return [phrase]
    
def generate_tree(phrase):
    """Generate a random sentence or phrase,
     with a complete parse tree."""
    if isinstance(phrase, list): 
        return map(generate_tree, phrase)
    elif phrase in grammar:
        return [phrase] + generate_tree(choice(grammar[phrase]))
    else: return [phrase]

def mappend(fn, list):
    "Append the results of calling fn on each element of list."
    return reduce(lambda x,y: x+y, map(fn, list))

def producers(constituent):
    "Argument is a list containing the rhs of some rule; return all possible lhs's"
    results = []
    for (lhs,rhss) in grammar.items():
	for rhs in rhss:
	    if rhs == constituent:
		results.append(lhs)
    return results

def printtable(table, wordlist):
    "Print the dynamic programming table.  The leftmost column is always empty."
    print "    ", wordlist
    for row in table:
	print row

def parse(sentence):
    "The CYK parser.  Return True if sentence is in the grammar; False otherwise"
    global grammar
    # Create the table; index j for rows, i for columns
    length = len(sentence)
    table = [None] * (length)
    trace = [None] * (length) 
    for j in range(length):
	table[j] = [None] * (length+1)
	trace[j] = [None] * (length+1) 
	for i in range(length+1):
	    table[j][i] = []
	    trace[j][i] = []  
  
    # Fill the diagonal of the table with the parts-of-speech of the words
    for k in range(1,length+1):
	values = producers(sentence[k-1])
	table[k-1][k].extend(values)
	#l = [] 
	#for value in values :
        #		trace[k-1][k].append([(k-1,k,values.index(value))])

    # initially the width is 2 start = 0 and mid = 1 to  
    for width in range(2,length+1):
	for start in range(0,length+1-width):
		end = start+width;
		for mid in range(start+1,end):
			for x in table[start][mid]:
				for y in table[mid][end]:
					table[start][end].extend(producers([x,y]))
					if producers([x,y])!=[]:  
						trace[start][end].extend([(start,mid,table[start][mid].index(x)),(mid,end,table[mid][end].index(y))])
    
    # Print the table
    printtable(table, sentence)
    
    if table[0][length]!=[]:
	for x in table[0][length]:
                print "Result : " + x
                print "Trace :"
                printtrace((0,length,table[0][length].index(x)),trace,table,sentence)
                print
        return True

    else :
        print " Sentence does not fit in the grammar "
        return False


def printtrace(index,trace,table,sentence):
    
    (x,y,z) = index 
    if (x +1 == y):
	print "['"+table[x][y][z]+"',"+"'"+sentence[x]+"']",
	return 
    
    print "['"+table[x][y][z]+"'",
    print ",",
    printtrace(trace[x][y][0],trace,table,sentence)
    print ",",
    printtrace(trace[x][y][1],trace,table,sentence)
    print "]",
    
    

def printlanguage ():
    "Randomly generate many sentences, saving and printing the unique ones"
    language = {}
    size = 0
    for i in range(100):
	sentencestr = ' '.join(generate('S'))
	language[sentencestr] = 1
	if len(language) > size:
	    size = len(language)
	    print '+',
	else:
	    print '.',
	    sys.stdout.flush()
	print
    for s in language.keys():
	print s
    print size

def printsentence ():
    print ' '.join(generate('S'))



#parse('dog with red pickles the dog'.split())
parse('see the dog'.split())
#parse('the big slept the pickles'.split())
#print generate_tree('S')
#print generate_tree('Q') 
#print generate_tree('I')
#print choice(grammar['S'])
#printlanguage()
