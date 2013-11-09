from dicts import DefaultDict
import glob 

def bigrams(words):
    """Given an array of words, returns a dictionary of dictionaries,
    containing occurrence counts of bigrams."""
    d = DefaultDict(DefaultDict(0))
    for (w1, w2) in zip([None] + words, words + [None]):
        d[w1][w2] += 1
 
    unigram = DefaultDict(0) ; 
    for word1 in d :        
      for word2 in d[word1]: 
	  unigram[word1]+= d[word1][word2] 

    print len(unigram) 
    #laplace smoothing 
    l=1
   
    for word1 in d : 
	for word2 in d[word1]:  
		d[word1][word2] = (float(d[word1][word2])+l)/(unigram[word1]+ (l*len(unigram)))
    return d 
def file2bigrams(filename):
    return bigrams(open(filename).read().split())

d = file2bigrams("gettysburgh")
print "The phrase 'world will' occurs with probability", d['world']['will']
print "The phrase 'shall not' occurs with probability", d['shall']['not']

def naivebayes(dirs) : 
     classes = []
     for dir in dirs : 
         for file in dir : 
		d =file2bigrams(file)	

def get_stats (poscount ,negcount,posacc,negacc) :
     print "STATISTICS"
     print "Size of the Vocabulary:" + str(len(vocab))
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
         if classify(nb,file)[0][1] == neglabel :
                neg_acc+=1 ;

    for file in postestfile :
        poscount+=1
        if classify(nb,file)[0][1] == poslabel :
                pos_acc+=1

    return (poscount,negcount,pos_acc,neg_acc)


if __name__ = "__main__" : 
	dirs = sys.argv[1:-2] 
        spamtest = sys.argv[-1] 
        hamtest = sys.argv[-2] 
        spamtest = glob.glob(spamtest+"/*"); 
        hamtest = glob.glob(hamtest+"/*"); 
        
        nb = naivebayes(dirs) 
        (poscount,negcount,smooth_pos_acc,smooth_neg_acc) = classification(nb,negtestfile,postestfile,"neg_clean","pos_clean")
        get_stats(poscount,negcount,smooth_pos_acc , smooth_neg_acc) ;

