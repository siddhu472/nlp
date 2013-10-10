import shutil 
import glob 
import os 
import sys 
inputdir = "/home/sid/Desktop/git/nlp/Assignment4/spamham/easy_ham_2/" 
outputdir = "/home/sid/Desktop/git/nlp/Assignment4/ham"
testdir = "/home/sid/Desktop/git/nlp/Assignment4/testing"
inputdir = glob.glob(inputdir+"/*")
totalcount = 1200 
count = 0 
for file in inputdir : 
	if count < totalcount : 
		shutil.copy(os.path.abspath(file),outputdir) 
	else: 
		shutil.copy(os.path.abspath(file),testdir) 
	count = count+1 

