from bs4 import BeautifulSoup
import requests


source = requests.get('https://almanakka.helsinki.fi/fi/liputus-ja-juhlapaivat/liputuspaivat-2018.html').text
soup = BeautifulSoup(source, 'lxml')
'''soup = BeautifulSoup(source, 'html.parser')'''

article = soup.find('article')
#print(article.prettify())
summary=article.find('div', itemprop='articleBody')

titles=[]

for headline in article.find_all('h3'):
    titles.append(headline.text)
'''
for day in article.find_all('p'):
    print(day.text)

if item in summaryList:
    print('TRUE')
'''
summaryList=summary.text.split('\n')
item=titles[0]
lineNumber=0
headlineAndLineNumber={}
lineHeadline=0

for lineHeadline in range(len(titles)):
    for i in summaryList:
        if i==titles[lineHeadline]:
            headlineAndLineNumber[i]=lineNumber
            lineNumber=0
            break;
        else:
            lineNumber+=1
    lineHeadline+=1

def flagDay(datee):
    flagDateList=[]
    flagD=None
    titleD=None
    try:
        dot=datee.find('.')
        x=int(datee[0:dot])
        y=int(datee[dot+1:dot+3])
        datee=(str(x)+'.'+str(y))
        
        
        if datee[-1]!='.':
            datee=datee+'.'
            
        dateLine=0
        
        for x in range(len(summaryList)-1):
            
            if datee in summaryList[x][0:len(datee)]:
                flagD=summaryList[x]
                #print(summaryList[x])
                break;
            else:
                dateLine+=1
                
        if dateLine<(len(summaryList)-2):
            if dateLine>=headlineAndLineNumber.get(titles[0]) and dateLine<headlineAndLineNumber.get(titles[1]):
                titleD=titles[0]
                
            elif dateLine>=headlineAndLineNumber.get(titles[1]) and dateLine<headlineAndLineNumber.get(titles[2]):
                titleD=titles[1]
                
            elif dateLine>=headlineAndLineNumber.get(titles[2]) and dateLine<headlineAndLineNumber.get(titles[3]):
                titleD=titles[2]
                
            elif dateLine>=headlineAndLineNumber.get(titles[3]) and dateLine<headlineAndLineNumber.get(titles[4]):
                titleD=titles[3]
                
            else:
                titleD=titles[4]
            print(titleD)
            print(flagD)
            flagDateList.append(titleD)
            flagDateList.append(flagD)
            return flagDateList
        else:
            #print("Couldn't find flag day")
            flagDateList.append(titleD)
            flagDateList.append(flagD)
            return flagDateList
    except:
        
        flagDateList.append(titleD)
        flagDateList.append(flagD)
        return flagDateList
    
#print(len(titles))
