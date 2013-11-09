import nltk 
import os 
from nltk.corpus import stopwords

def removeStopwords(data): 
  word_list = data.split()
  filtered_words = [w for w in word_list if not w in stopwords.words('english')]
  print filtered_words 
  return ' '.join(filtered_words)


inputpath = "/home/sid/Desktop/git/nlp/Assignment4/reviews /txt_sentoken/pos"  
outputpath = "/home/sid/Desktop/git/nlp/Assignment4/reviews /txt_sentoken/pos_clean" 
filename = "pos" 
filecount = 0 ; 
fileExtension=".txt"; 
for file in os.listdir(inputpath): 
   f = open(inputpath+"/"+file) 
   content = f.read() 
   rawtext = nltk.clean_html(content) 
   cleandata = removeStopwords(rawtext); 
   f1 = open(outputpath+"/"+filename+str(filecount)+fileExtension,"w"); 
   f1.write(cleandata) 
   filecount+=1 ; 
   f.close() 
   f1.close()

print "done"  


