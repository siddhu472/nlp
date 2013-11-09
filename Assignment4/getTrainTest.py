import shutil 
import glob 
import os 
import sys 
inputdir = "/home/sid/Desktop/git/nlp/Assignment4/reviews /txt_sentoken/pos_clean/" 
outputdir = "/home/sid/Desktop/git/nlp/Assignment4/pos_clean_max"
testdir = "/home/sid/Desktop/git/nlp/Assignment4/testing/pos_clean_max"
inputdir = glob.glob(inputdir+"/*")
totalcount = 975
count = 0 
for file in inputdir : 
	if count < totalcount : 
		shutil.copy(os.path.abspath(file),outputdir) 
	else: 
		shutil.copy(os.path.abspath(file),testdir) 
	count = count+1 

