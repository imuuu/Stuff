
    
#import os.path
import random
save_path= 'C:/example/'

def addJoke(joke,name='noName'):
    
    
    file = open('jokes.txt','a')
    file.write('\n'+name+' . '+joke)
    
    file.close()
    print("Joke added")
    

def removeSpace(string,position,seperator):
    dotPosition=position
    newS=string
    x=1
    kpl=0
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
            if kpl>1000:
                x=1
        kpl+=1
    return newS
def readSpecificJoke(jokeName):
    file=open('jokes.txt','r')
    filelist=file.read().split('\n')
    line=0
    for i in filelist:
        
        if i.find('.')>0:
            dotposition=i.find('.')
            str=removeSpace(i, dotposition, '.')
            dotposition=i.find('.')
            nameOfjoke=str[:dotposition-1]
            
            jokeName=jokeName.upper()
            nameOfjoke=nameOfjoke.upper()
            
            if nameOfjoke==jokeName:
                listOfjoke=giveJoke(line)
                return  listOfjoke
                break
                
        line+=1  
def makeJoke(joke):
    
    dotPosition=joke.find('.')
    jokeAnswer=False
    if joke.find(':')>0:
        colonPosition=joke.find(':')
        newS=removeSpace(joke, colonPosition, ':')
        jokeAnwser=newS[colonPosition:]
        jokeAnswer=True
    else:
        colonPosition=len(joke)
        jokeAnwser=None
        newS=joke
    
    newS=removeSpace(newS, dotPosition, '.')
     
    dotPosition=newS.find('.')
    
    nameJoke=newS[:dotPosition]
    if jokeAnswer==False:
        shownJoke=newS[(dotPosition+1):(colonPosition-2)]
    else:
        shownJoke=newS[(dotPosition+1):(colonPosition-3)]
        
    
    listOfjoke=[nameJoke,shownJoke,jokeAnwser] 
    return listOfjoke    
def giveJoke(line):
    file=open('jokes.txt','r')
    filelist=file.read().split('\n')
    
    if not filelist[0]:
        filelist.pop(0)
    
    joke=filelist[line]
    dotPosition=joke.find('.')
    jokeAnswer=False
    if joke.find(':')>0:
        colonPosition=joke.find(':')
        newS=removeSpace(joke, colonPosition, ':')
        jokeAnwser=newS[colonPosition:]
        jokeAnswer=True
    else:
        colonPosition=len(joke)
        jokeAnwser=None
        newS=joke
    
    newS=removeSpace(newS, dotPosition, '.')
     
    dotPosition=newS.find('.')
    
    nameJoke=newS[:dotPosition]
    if jokeAnswer==False:
        shownJoke=newS[(dotPosition+1):(colonPosition-2)]
    else:
        shownJoke=newS[(dotPosition+1):(colonPosition-3)]
        
    
    listOfjoke=[nameJoke,shownJoke,jokeAnwser] 
    return listOfjoke    
def readrandomJoke():
    try:
        file=open('jokes.txt','r')
        filelist=file.read().split('\n')
        
        if not filelist[0]:
            filelist.pop(0)
        
        numberOflines=len(filelist) #start at 1
        
        if numberOflines>0:
            line=random.randint(1,(numberOflines-1))
            listOfjoke=giveJoke(line)
            
            return listOfjoke
    except:
        file=open('jokes.txt','a')
        file.close()
        print("There wasn't jokes.txt so I made it")
        
        
    
    
'''
def main():
    #addJoke('pää : ei ole','iso')
    #readJoke()
    #print(readSpecificJoke('lie'))
    #print(readrandomJoke())
main()
'''