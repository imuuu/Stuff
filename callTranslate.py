from bs4 import BeautifulSoup
import requests 

def translatorRobot(language,languageTo,word):
    
    source = requests.get('https://translate.google.com/m?hl='+languageTo+'&sl='+language+'&tl='+languageTo+'&ie=UTF-8&prev=_m&q='+word+'').text
    soup = BeautifulSoup(source, 'lxml')
    row1=soup.find('div', dir="ltr")
    return row1.text

print(translatorRobot('fi', 'ru', 'hei'))