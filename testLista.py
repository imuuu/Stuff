
    
import os.path
import random
save_path= 'C:/example/'

def addJoke(joke,name='noName'):
    
    
    file = open('jokes.txt','a')
    file.write('\n'+name+' . '+joke)
    
    file.close()
    print("Done")
    

def removeSpace(string,position,seperator):
    dotPosition=position
    newS=string
    x=1
    while x>0:
        if (newS[dotPosition-1])==" ":
            newS=newS[:dotPosition-1]+newS[dotPosition:]
            
        dotPosition=newS.find(seperator)
        
        if (newS[dotPosition+1])==" ":
            newS=newS[:dotPosition]+seperator+newS[dotPosition+2:]
        
        if newS[dotPosition-1]==" " or newS[dotPosition+1]==" ":
            x=1
        else:
            x=0
    return newS
    
def readJoke():
    file=open('jokes.txt','r')
    filelist=file.read().split('\n')
    
    if not filelist[0]:
        filelist.pop(0)
    
    numberOflines=len(filelist) #start at 1
    
    if numberOflines>0:
        line=random.randint(1,(numberOflines-1))
        joke=filelist[line]
        dotPosition=joke.find('.')
        if joke.find(':')>0:
            colonPosition=joke.find(':')
        else:
            colonPosition=len(joke)
        
        newS=removeSpace(joke, dotPosition, '.')
        newS=removeSpace(newS, colonPosition, ':')
        print(newS)
        
        dotPosition=newS.find('.')
        colonPosition=newS.find(':')
        
        nameJoke=newS[:dotPosition]
        shownJoke=newS[(dotPosition+1):(colonPosition)]
        jokeAnwser=newS[colonPosition+1:]
        
        
        print(nameJoke)
        print(shownJoke)
        print(jokeAnwser)
        print(dotPosition)
        print(colonPosition)
        
        
        
    
    

def main():
    addJoke('pää : ei ole','iso')
    readJoke()
    
main()