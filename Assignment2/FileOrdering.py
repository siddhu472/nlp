import shutil ; 

f = open("SPAMTrain.label","r"); 
spam = []
ham = [] 
for line in f:
    words = line.split() 
    if(words[0]=="0"):
      spam.append(words[1]); 
    if(words[0]=="1"):
      ham.append(words[1]); 

print spam 
print ham 

for file in spam: 
   source ="./Data/"+file ; 
   destination="./SpamFull/"+file ;  
   shutil.move(source,destination) ; 

for file in ham: 
  source="./Data/"+file ; 
  destination="./hamFull/"+file ; 
  shutil.move(source,destination); 
          
