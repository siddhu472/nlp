import re
import sys
from dicts import DefaultDict
from random import choice
import math
import operator 

wordcounts = DefaultDict(0)  
tp = DefaultDict(0) # True Positives 
fp  =DefaultDict(0) # False Positives 
fn = DefaultDict(0) # False Negatives 
precision = DefaultDict(0) # Precision 
recall = DefaultDict(0) #Recall 
fscore = DefaultDict(0) #FScore 

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
	    		#tag = compose(tag) # to compose the tags 
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

    l=0.01 # smoothing parameter  
    for tag,dict in emissions.items():
	emissions[tag]['<UNKNOWN>'] = l 
	for word,count in dict.items():
	    if wordcounts[word] == 1:
		del emissions[tag][word]
		 
    
    # Here you need to add code that will turn these dictionaries 
    # of counts into dictionaries of smoothed conditional probabilities
    
    smoothingconstant1 = len(transitions) 
    # To find the transition probabilities 
    for tag1,tag2 in transitions.items(): 
	  sum = 0 ;  
	  for tag2 in transitions[tag1]:
 		sum+= transitions[tag1][tag2] 
	  for tag2 in transitions[tag1]:
		#Applying laplace smoothing  	
		transitions[tag1][tag2] = float(transitions[tag1][tag2]+l)/(sum+l*smoothingconstant1) 


    # To find the emission probabilities 
    smoothingconstant2 = len(transitions)    
    for tag,word in emissions.items(): 
	 sum = 0 ;
	 for word in emissions[tag]:
		sum+= emissions[tag][word] 
	 for word in emissions[tag] : 
		emissions[tag][word] = float(emissions[tag][word]+l)/(sum+l*smoothingconstant2)      

    return (transitions, emissions)
	    
def viterbi_tags (wordarray,transitions,emissions):
    """Given a string containing the space-separated words of a sentence;
    (there should even be spaces on either side of punctuation, as in the
    WSJ training data), return an array containing the mostl likely
    sequence of part-of-speech tags."""
    # Implement Viterbi here
    # return the mostly likely sequence of part-of-speech tags
   
    # inititalize viterbi  
    viterbi = DefaultDict(DefaultDict(0)) 
    viterbi["START"][0] = 1 

    # Set all new words in the test to <UNKNOWN>
    for i in range(0,len(wordarray)) : 
	if wordarray[i]  not in wordcounts.keys():
             wordarray[i] = "<UNKNOWN>"

    # This Data structure maintains the backpointers for each input word 
    backtrack = DefaultDict(DefaultDict(0)) 

    tags = [] 
    for tag in transitions.keys():
	tags.append(tag)

    for t in range(0,len(wordarray)): 
	for tag in tags : 
		for nexttag in transitions[tag]:
                        if emissions[nexttag][wordarray[t]] ==0 : 
				emission = emissions[nexttag]['<UNKNOWN>'] 
			else :
				emission = emissions[nexttag][wordarray[t]] 
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
    
    likelysequence = [0]*len(wordarray) 
    for t in range(len(wordarray),0,-1):
    	likelysequence[t-1] =  resultTag  
    	prevtag = backtrack[resultTag][t] 
     	resultTag = prevtag
 
    return likelysequence,result


def true_tags (tagged_sentence):
    """Given a string containing the space-separated words/POS of a sentence;
    (there should even be spaces on either side of punctuation, as in the
    WSJ training data) pull out and return the tag sequence and the word sequence seperately ."""
    wordarray = tagged_sentence.split()
    tags = [word.split('/')[1] for word in wordarray]
    words = [word.split('/')[0] for word in wordarray] 
    return (words,tags)

def compose(tag): 
        """ Given a tag , if the tag is a VB* or JJ* or NN* or RB* , it returns the base type . 
	if its none of the above mentioned types it returns the tag back """
	patternVB = "^VB"	
	patternJJ = "^JJ"
	patternNN = "^NN"
	patternRB = "^RB"
	progVB = re.compile(patternVB) 
	progJJ = re.compile(patternJJ) 
	progNN = re.compile(patternNN) 
	progRB = re.compile(patternRB)
	
	if(progVB.match(tag)):
		output =  "VB" 
	elif(progJJ.match(tag)):
		output = "JJ" 
	elif(progNN.match(tag)):
		output = "NN"
	elif(progRB.match(tag)):
		output = "RB"
	else : 
		output = tag

	return output 

def forward(wordarray,transitions,emissions): 
	forward = DefaultDict(DefaultDict(0))
	forward["START"][0] = 1 
	tags = []
    	for tag in transitions.keys():
        	tags.append(tag)

    	defaultTransitionProb = DefaultDict(0)
    	for tag in tags :
        	tsum = 0 ;
        	for tag2 in transitions[tag]:
                	tsum+=transitions[tag][tag2]
        	defaultTransitionProb[tag] = (0.01)/(tsum+0.01*len(tags))

    	for t in range(0,len(wordarray)):
        	for tag in tags :
                	for nexttag in transitions[tag]:
                        	if transitions[tag][nexttag] == 0 :
                                	transition = defaultTranitionProb[tag]
                        	else:
                           		transition = transitions[tag][nexttag]
                        	if emissions[nexttag][wordarray[t]] ==0 :
                                	emission = emissions[nexttag]['<UNKNOWN>']
                        	else :
                                	emission = emissions[nexttag][wordarray[t]]
                        	forward[nexttag][t+1] = forward[nexttag][t+1] + forward[tag][t]*transition*emission
	return forward

def backward(wordarray,transitions,emissions):
	backward  = DefaultDict(DefaultDict(0))
        backward["START"][len(wordarray)] = 1
        tags = []
        for tag in transitions.keys():
                tags.append(tag)
        
        defaultTransitionProb = DefaultDict(0)
        for tag in tags :
                tsum = 0 ;
                for tag2 in transitions[tag]:
                        tsum+=transitions[tag][tag2]
                defaultTransitionProb[tag] = (0.01)/(tsum+0.01*len(tags))
        
        for t in range(len(wordarray),-1,-1):
                for tag in tags :
                        for nexttag in transitions[tag]:
                                if transitions[tag][nexttag] == 0 :
                                        transition = defaultTranitionProb[tag]
                                else:
                                        transition = transitions[tag][nexttag]
                                if emissions[nexttag][wordarray[t]] ==0 :
                                        emission = emissions[nexttag]['<UNKNOWN>']
                                else :
                                        emission = emissions[nexttag][wordarray[t]]
                                backward[nexttag][t+1] = forward[nexttag][t+1] + forward[tag][t]*transition*emission
        return forward

def getConfidentSentences(confidence,obtainedPOS,high=False):
        """ Returns the most confident or the least confident sentences based on the last parameter . The 
	inputs are the confidence for each sentences and the POS tags obtained from the HMM POS tagger """ 
     	sorted_confidence = sorted(confidence.iteritems(), key=operator.itemgetter(1))
	if high == True:
		sorted_confidence.reverse(); 
		print "High confidence sentences :" ; 
   	else :
		print "Low confidence sentences : " ; 
    	count = 0; 
    	for sentence,prob in sorted_confidence:
        	if count>10: 
           		break ;  
        	count = count+1
        	print "Confidence :" + str(prob) + "Original Sentence:" + sentence 
        	print " Obtained POS " , 
       	 	print obtainedPOS.get(sentence)  

 
def calculateAccuracy (expected,obtained):
	correct = 0 ;
	for x,o in zip(expected,obtained):
		    if x == o :
			correct = correct+1 
			tp[x] +=1  
		    else:  
			fn[x] +=1 
			fp[o] +=1 
	print correct ,
	print " " , 
	print len(expected) 
	return correct,len(expected)	

if __name__ == '__main__':
    #print "Usage:", sys.argv[0], "wsjtrainfile wsjtestfile"
    trainfile = sys.argv[1]
    testfile = sys.argv[2]
    h = hmm (open(trainfile))
    f = open(testfile)
  
    totalcorrect = 0 
    ttotal = 0  
    confidence = DefaultDict(0); # confidence of the sentences  
    obtainedPOS = DefaultDict(0) ; # The tags produced by the HMM POS tagger 
 
    for line in f.xreadlines():
    	(words,expected) = true_tags(line)  
    	(result,prob) = viterbi_tags(words,h[0],h[1])	
	forward(words,h[0],h[1]) 
	backward(words,h[0],h[1])
	conf = math.pow(prob,(1.0/len(expected))) ; 
	confidence[line] = conf
    	obtainedPOS[line] = result 
	(correct,total) = (calculateAccuracy(expected,result))	 
	totalcorrect+=correct 
	ttotal+=total 
   
    
    for tag in tp.keys():
	precision[tag] = float(tp[tag])/(tp[tag]+fp[tag]);
	recall[tag] = float(tp[tag])/(tp[tag]+fn[tag]); 
	fscore[tag] = (2 * precision[tag]*recall[tag])/(precision[tag]+recall[tag])

    print " Precision Recall FScore"
    for tag in precision.keys():
	print tag, 
	print round(precision[tag]*100,2), 
	print " ",
	print round(recall[tag]*100,2), 
	print " ", 
	print round(fscore[tag]*100,2) 


    print "Accuracy:" + str(round((float(totalcorrect)/ttotal)*100,3))
    
    
    getConfidentSentences(confidence,obtainedPOS)  
    getConfidentSentences(confidence,obtainedPOS,True) 
