# This code should help get you started, but it is not guaranteed to
# be bug free!  If you find problems, please report to
# compling-class@cs.umass.edu

import sys
from dicts import DefaultDict
from random import choice
import math 

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
    wordcounts = DefaultDict(0)
    # For each sentence (one per line)
    for line in file.xreadlines():
	# for each word in the sentence (space separated)
 	prevtag = 'START'   # Before each sentence, begin in START state
	for taggedword in line.split():
	    if(len(taggedword.split('/')) == 2):
	    	(word, tag) = taggedword.split('/')
		if tag.isalpha():
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


    smoothingconstant2 = len(emissions) 
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
    #wordarray = untagged_sentence.split()
    # Implement Viterbi here
    # return the mostly likely sequence of part-of-speech tags
   
    '''    			
    tags = [] 
    for tag in transitions.keys():
	tags.append(tag) 
     
    viterbi = DefaultDict(DefaultDict(0))
    backtrack = DefaultDict(DefaultDict(0))

    viterbi["START"][0] = 1 
    for t in range(0,len(wordarray)-1):
	for tag in tags :
		for nexttag in transitions[tag]:
			score = viterbi[tag][t]*transitions[tag][nexttag]*emissions[nexttag][wordarray[t]]
			if (viterbi[nexttag][t+1] == 0 or  score > viterbi[nexttag][t+1]):
				viterbi[nexttag][t+1] = score 
				backtrack[nexttag][t+1] = tag 
   
    for tag in viterbi.keys():
	print tag + ":" , 
	print  viterbi[tag]  
    for tag in  backtrack.keys():
	print tag +":" , 
	print  backtrack[tag]  
    '''
    # inititalize delta 
    delta = DefaultDict(list) 
    for tag1,tag2 in transitions.items() : 
	delta[tag1] = [0]*(len(wordarray)+1)
    delta["START"][0] = 1 

    backtrack = DefaultDict(list) 
    for tag1,tag2 in transitions.items() : 
	backtrack[tag1] = [0]*(len(wordarray)+1)	
    #print delta    
    # induction

    tags = [] 
    for tag1,tag2 in transitions.items():
	tags.append(tag1)

    #print tags   
    for tag in tags : 
	for t in range(1,len(wordarray)+1):
		maxVal = 0 ; 
	 	maxState = "UNDEFINED"; 
		for prevtag in tags :
			if emissions[tag][wordarray[t-1]] == 0 : 
				emissionprob = emissions[tag]["<UNKNOWN>"]  
			else :
				emissionprob = emissions[tag][wordarray[t-1]]
			if(maxVal < transitions[prevtag][tag]*delta[prevtag][t-1] * emissionprob):
				maxVal = transitions[prevtag][tag] * delta[prevtag][t-1] * emissionprob
				maxState = prevtag
		delta[tag][t] = maxVal
		backtrack[tag][t] = maxState  
    
    print delta 	
    print backtrack 

   
    # Termination and path readout  
    result = 0 
    resultTag = "UNDEFINED " 
    for tag in tags : 
	if(delta[tag][len(wordarray)] > result):
		result = delta[tag][len(wordarray)]
		resultTag = tag 
    
    print result  
    likelysequence = [0]*len(wordarray) 
    for t in range(len(wordarray),0,-1):
    	likelysequence[t-1] =  resultTag  
    	prevtag = backtrack[resultTag][t] 
     	resultTag = prevtag
 
    print likelysequence 
    '''
    likelysequence2 = [] 
    for t in range(1,len(wordarray)+1):
	max = 0 ; 
	state = "UNDEFINED"
	for tag in tags:
		if(delta[tag][t] > max):
			max = delta[tag][t] 
			state = tag 
	likelysequence2.append(state) 
		 
    return likelysequence2 
    '''
    #print likelysequence 	
    #return likelysequence 

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
	print expected 
	print obtained 
	for x,o in zip(expected,obtained):
		  if x == o :	
			correct = correct+1 
	return float(correct)/len(expected)	

if __name__ == '__main__':
    #print "Usage:", sys.argv[0], "wsjtrainfile wsjtestfile"
    #dirs = sys.argv[1:-1]
    #testfile = sys.argv[-1]
    #h = hmm (sys.stdin)
    #dirs = "wsj15-18.pos"
    h = hmm (open("sample"))
    #f = open("test2")
    #for line in f.xreadlines():
    #	(words,expected) = true_tags(line)  
    # 	result = viterbi_tags(words,h[0],h[1])
    #	print "Accuracy:" + str(calculateAccuracy(expected,result))	 
    #sentence  = "b a d" 
    result = viterbi_tags(["b","a","d"],h[0],h[1])
    print result
    #print h[0]
    #print '------'
    #print h[1]
    #(a,expected) = true_tags ('a/P b/Q s/P')
    #print "Accuracy:" + str(calculateAccuracy(expected,result))
