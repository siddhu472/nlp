#!/sw/bin/python

import math
import sys
import glob
import pickle
from dicts import DefaultDict
from sets import Set 

# In the documentation and variable names below "class" is the same
# as "category"

vocab = Set() 


def bigrambayes (dirs):
    """Train and return a bigram Bayes classifier.  
    The datastructure returned is an array of tuples, one tuple per
    class; each tuple contains the class name (same as dir name)
    and the multinomial distribution over words associated with
    the class and the number of words in the class"""
    classes = []
    number_of_classes = len(dirs) ; 
    
    for dir in dirs : 
	#countdict =  files2countdict(glob.glob(dir+"/*"))
	(countdict,unigramcount)  = files2bigramdict(glob.glob(dir+"/*"))
        classes.append((dir,countdict,unigramcount))
    return classes

def classify (classes, filename):
    """Given a trained naive Bayes classifier returned by naivebayes(), and
    the filename of a test document, d, return an array of tuples, each
    containing a class label; the array is sorted by log-probability 
    of the class, log p(c|d)"""
    answers = []
    #print 'Classifying', filename
    for c in classes:
	score = 0
        # laplace smoothing
	# to take care of all the unknown words , we find the size of the vocabulary and add that to the wordcount in classes 
	allwordcounts = 0 ; 
	for w in c[2] : 
		allwordcounts+= c[2][w] 
	allwordcounts += len(vocab)

	# The probabilities of all the unknown words 
	unknown_wordprob = 1.0/allwordcounts ; 

	words = open(filename).read().split()
        for (w1,w2) in zip([None] + words,words +[None]): 
	    if (c[1].get(w1)): 
	    	count = c[1].get(w1).get(w2)
	    	if (count>0):
			x = math.log(count); 
		else :
			x = math.log(unknown_wordprob)
	    else : 
		x = math.log(unknown_wordprob) 	
	    score+=x ; 		
	answers.append((score,c[0]))
    answers.sort()
    return answers

def files2bigramdict (files): 
    d = DefaultDict(DefaultDict(0))
    for file in files:
        words =  open(file).read().split()
        for (w1, w2) in zip([None] + words, words + [None]):
            if w1 not in vocab : 
		vocab.add(w1) 
	    if w2 not in vocab :
		vocab.add(w2) 
	    d[w1][w2] += 1
    
    unigram = DefaultDict(0) ;
    for word1 in d :
      for word2 in d[word1]:
          unigram[word1]+= d[word1][word2]

    #laplace smoothing  
    for word1 in d :
        for word2 in d[word1]:
                d[word1][word2] = (float(d[word1][word2])+1)/(unigram[word1]+len(unigram))
     
    # we return the probability (word1,word2|class) = (number of word1,word2 pair in c)/(number of word1 * pair in c)  
    return (d,unigram)


def get_stats (poscount ,negcount,posacc,negacc) : 
     print "STATISTICS"
     print "Number of positive review files:" + str(negcount)
     print "Number of negative review  files:" + str(poscount)
     print "Number of negative reviews identified as negative:" + str(negacc)
     print "Number of positive reviews  identified as positive:" + str(posacc)
     print "negative accuracy:" + str(float(negacc)/negcount)
     print "positve accuracy:" + str(float(posacc)/poscount)
     accuracy = float(posacc+negacc)/(poscount+negcount)
     print "Overall accuracy:" + str(accuracy)
     recall = float(posacc)/poscount
     print "Recall" + str(recall)
     precision = float (posacc)/(posacc+(negcount-negacc))
     print "Precision:" + str(precision)
     print "F1 Score:" + str((2*precision*recall)/(precision+recall))
   
def classification(nb,negtestfile,postestfile,neglabel,poslabel) :
    negcount = 0
    poscount = 0
    neg_acc = 0
    pos_acc = 0
    for file in negtestfile :
         negcount+=1
         if classify(nb,file)[1][1] == neglabel :
                neg_acc+=1 ;

    for file in postestfile :
        poscount+=1
        if classify(nb,file)[1][1] == poslabel :
                pos_acc+=1
 
    return (poscount,negcount,pos_acc,neg_acc)    	


if __name__ == '__main__':
    print 'argv', sys.argv
    print "Usage:", sys.argv[0], "classdir1 classdir2 [classdir3...] pos_test neg_test"
    dirs = sys.argv[1:-2]
    negtestfile = sys.argv[-1]
    postestfile = sys.argv[-2]
    negtestfile = glob.glob(negtestfile+"/*")  
    postestfile = glob.glob(postestfile+"/*") 
		 
nb = bigrambayes(dirs)
(poscount,negcount,smooth_pos_acc,smooth_neg_acc) = classification(nb,negtestfile,postestfile,"neg","pos")
get_stats(poscount,negcount,smooth_pos_acc , smooth_neg_acc) ; 



