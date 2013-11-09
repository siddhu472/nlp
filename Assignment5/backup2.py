# This code should help get you started, but it is not guaranteed to
# be bug free!  If you find problems, please report to
# compling-class@cs.umass.edu

import sys
from dicts import DefaultDict
from random import choice
import math

wordcounts = DefaultDict(0)  

def Dict(**args): 
    """Return a dictionary with argument names as the keys, 
    and argument values as the key values"""
    return args

def hmm (file):
    """Given an open FILE, e.g. from the open(filename) function,
    Read pre-tagged sentences of WSJ, one per line.  Return an HMM,
    here represented as a tuple containing (1) the transition probabilities,
    and (2) the emmission probabilities."""
    transitions = DefaultDict(DefaultDict(0))
    emissions = DefaultDict(DefaultDict(0))
    # For each sentence (one per line)
    for line in file.xreadlines():
	# for each word in the sentence (space separated)
 	prevtag = 'START'   # Before each sentence, begin in START state
	for taggedword in line.split():
		if len(taggedword.split('/'))==2:
	    		(word, tag) = taggedword.split('/')
	    		transitions[prevtag][tag] += 1
	    		emissions[tag][word] += 1
	    		wordcounts[word] += 1
	    		prevtag = tag

    # At test time we will need estimates for "unknown words"---the words
    # the words that never occurred in the training data.  One recommended
    # way to do this is to turn all training words occurring just once 
    # into '<UNKNOWN>' and use this as the stand-in for all "unknown words"
    # at test time.  Below we make all the necessary transformations
    # to '<UNKNOWN>'.
    for tag,dict in emissions.items():
	for word,count in dict.items():
	    if wordcounts[word] == 1:
		del emissions[tag][word]
		emissions[tag]['<UNKNOWN>'] += 1

    # Here you need to add code that will turn these dictionaries 
    # of counts into dictionaries of smoothed conditional probabilities

    #l = 0 
    #smoothingconstant1 = 0 	
    l = 1 
    smoothingconstant1 = len(transitions) 
    # To find the transition probabilities 
    for tag1,tag2 in transitions.items(): 
	  sum = 0 ;  
	  for tag2 in transitions[tag1]:
 		sum+= transitions[tag1][tag2] 
	  for tag2 in transitions[tag1]:
		#Applying laplace smoothing  	
		transitions[tag1][tag2] = float(transitions[tag1][tag2]+l)/(sum+smoothingconstant1) 


    #smoothingconstant2 = len(emissions) 
    # To find the emission probabilities 
    for tag,word in emissions.items(): 
	 sum = 0 ;
	 for word in emissions[tag]:
		sum+= emissions[tag][word] 
	 for word in emissions[tag] : 
		emissions[tag][word] = float(emissions[tag][word])/(sum)      

    return (transitions, emissions)
	    
def viterbi_tags (wordarray,transitions,emissions):
    """Given a string containing the space-separated words of a sentence;
    (there should even be spaces on either side of punctuation, as in the
    WSJ training data), return an array containing the mostl likely
    sequence of part-of-speech tags."""
    # Implement Viterbi here
    # return the mostly likely sequence of part-of-speech tags
   
    # inititalize delta 
    viterbi = DefaultDict(DefaultDict(0)) 
    viterbi["START"][0] = 1 

    for i in range(0,len(wordarray)) : 
	if wordarray[i]  not in wordcounts.keys():
             wordarray[i] = "<UNKNOWN>"

    backtrack = DefaultDict(DefaultDict(0)) 

    tags = [] 
    for tag in transitions.keys():
	tags.append(tag)

    for t in range(0,len(wordarray)): 
	for tag in tags : 
		for nexttag in transitions[tag]:
			if emissions[nexttag][wordarray[t]] == 0 : 
				sum = 0 ; 
				for word in emissions[nexttag] : 
					sum+= emissions[nexttag][word] 
				emission = 1.0/(sum+len(tags)-1) 
			else: 	
				emission = emissions[nexttag][wordarray[t]]
			if transitions[tag][nexttag] == 0 : 
				sum = 0 ; 
				for tag2 in transitions[tag]:
					sum+= transitions[tag][tag2]  
				transition = 1.0/(sum+len(tags))
			else: 
			   transition = transitions[tag][nexttag] 
                        score = viterbi[tag][t]*transitions[tag][nexttag]*emission 
			if score > viterbi[nexttag][t+1] or viterbi[nexttag][t+1] ==0 :
				 viterbi[nexttag][t+1] = score 
				 backtrack[nexttag][t+1] = tag 


    # Termination and path readout  
    result = 0 
    resultTag = "UNDEFINED" 
    for tag in tags : 
	if(viterbi[tag][len(wordarray)] > result):
		result = viterbi[tag][len(wordarray)]
		resultTag = tag 
    

    if resultTag == "UNDEFINED":
	print "some error" 

    #print result  
    likelysequence = [0]*len(wordarray) 
    for t in range(len(wordarray),0,-1):
    	likelysequence[t-1] =  resultTag  
    	prevtag = backtrack[resultTag][t] 
     	resultTag = prevtag
 
    #print viterbi 
    #print backtrack 
    #print likelysequence 
    return likelysequence 

def true_tags (tagged_sentence):
    """Given a string containing the space-separated words/POS of a sentence;
    (there should even be spaces on either side of punctuation, as in the
    WSJ training data) pull out and return the tag sequence."""
    wordarray = tagged_sentence.split()
    tags = [word.split('/')[1] for word in wordarray]
    words = [word.split('/')[0] for word in wordarray] 
    return (words,tags)


def calculateAccuracy (expected,obtained):
	correct = 0 ;
	#print expected 
	#print obtained 
	global tcorrect 
	global ttotal
	for x,o in zip(expected,obtained):
		  if x == o :	
			correct = correct+1
			tcorrect = tcorrect + 1 
	ttotal += len(expected)  
	return float(correct)/len(expected)	

if __name__ == '__main__':
    #print "Usage:", sys.argv[0], "wsjtrainfile wsjtestfile"
    #dirs = sys.argv[1:-1]
    #testfile = sys.argv[-1]
    #h = hmm (sys.stdin)
    #dirs = "wsj15-18.pos"
    global tcorrect  
    global ttotal 
    tcorrect = ttotal = 0  
    h = hmm (open("training2"))
    f = open("test2")
    for line in f.xreadlines():
    	(words,expected) = true_tags(line)  
    	result = viterbi_tags(words,h[0],h[1])
    	print "Accuracy:" + str(calculateAccuracy(expected,result))	 
    #sentence  = "b a d" 
    #result = viterbi_tags(["b","e","a","d"],h[0],h[1])
    print result
    #print h[0]
    #print '------'
    #print h[1]
    #(a,expected) = true_tags ('a/P b/Q s/P')
    #print "Accuracy:" + str(calculateAccuracy(expected,result))
    print float(tcorrect)/ttotal 
