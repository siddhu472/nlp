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


def naivebayes (dirs,smooth=True):
    """Train and return a naive Bayes classifier.  
    The datastructure returned is an array of tuples, one tuple per
    class; each tuple contains the class name (same as dir name)
    and the multinomial distribution over words associated with
    the class"""
    classes = []
    number_of_classes = len(dirs) ; 
    for dir in dirs : 
	countdict =  files2countdict(glob.glob(dir+"/*"))
    for dir in dirs:
	countdict = files2countdict(glob.glob(dir+"/*"))
	# Here turn the "countdict" dictionary of word counts into
	# into a dictionary of smoothed word probabilities
	l = 1
	totalWordsInClass = 0 ; 
	totalWordsInClassSmooth = 0 ; 
	# laplace smoothing , if smooth is set to false , no smoothing is performed 
	for key in countdict : 
		totalWordsInClass += countdict[key] 
	for key in countdict: 
                if(smooth == False): 
		  totalWordsInClassSmooth = totalWordsInClass 
                  countdict[key] = float(countdict[key])/(totalWordsInClass) 
                else: 
	          totalWordsInClassSmooth = totalWordsInClass + l*len(vocab) 
		  countdict[key] = float(countdict[key]+l)/(totalWordsInClassSmooth) 
	classes.append((dir,countdict,smooth,totalWordsInClassSmooth))
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
	for word in open(filename).read().split():
	    word = word.lower()
            score += math.log(c[1].get(word,(1.0/c[3])))
	answers.append((score,c[0]))
    answers.sort()
    return answers

def files2countdict (files):
    """Given an array of filenames, return a dictionary with keys
    being the space-separated, lower-cased words, and the values being
    the number of times that word occurred in the files."""
    d = DefaultDict(0)
    for file in files:
	for word in open(file).read().split():
            if word.lower() not in  vocab: 
		vocab.add(word.lower())
	    d[word.lower()] += 1
    return d

def get_stats (poscount ,negcount,posacc,negacc) : 
     print "STATISTICS"
     print "Size of the Vocabulary:" + str(len(vocab))
     print "Number of neg test files:" + str(negcount)
     print "Number of pos test  files:" + str(poscount)
     print "Number of neg identified as neg:" + str(negacc)
     print "Number of pos  identified as pos:" + str(posacc)
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


# For running tests on a single file 
'''

if __name__ == '__main__': 
	dirs = sys.argv[1:-1]
	testfile = sys.argv[-1]  
	nb = naivebayes(dirs,False) 

	print classify(nb,testfile)
	print classify(nb,testfile)[1][1]
	print classify(nb,testfile)[1][0] 
'''

# for performing classification

if __name__ == '__main__':
    print 'argv', sys.argv
    print "Usage:", sys.argv[0], "classdir1 classdir2 [classdir3...] pos_test neg_test"
    dirs = sys.argv[1:-2]
    negtestfile = sys.argv[-1]
    postestfile = sys.argv[-2]
    negtestfile = glob.glob(negtestfile+"/*")  
    postestfile = glob.glob(postestfile+"/*") 
		 
print " With SMOOTHING "
nb = naivebayes(dirs)
# the parameters for classification are the labels 
(poscount,negcount,smooth_pos_acc,smooth_neg_acc) = classification(nb,negtestfile,postestfile,"neg_clean","pos_clean")
get_stats(poscount,negcount,smooth_pos_acc , smooth_neg_acc) ; 
print " Without SMOOTHING "
nb = naivebayes(dirs,False) 
(poscount,negcount,pos_acc,neg_acc) = classification(nb,negtestfile,postestfile,"neg_clean","pos_clean") 
get_stats(poscount,negcount,pos_acc,neg_acc) ; 



