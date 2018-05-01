from bs4 import BeautifulSoup
import requests

source = requests.get('http://ilmatieteenlaitos.fi/paikallissaa').text
soup = BeautifulSoup(source, 'lxml')

row1=soup.find('div', class_='mid local-weather-forecast meteogram selected table-responsive')

asteet=row1.find('tr', class_="meteogram-temperatures")
kellonajat=row1.find('tr', class_="meteogram-times")
paivat=row1.find('tr', class_="meteogram-dates")

days=[]
times=[]
temperatures=[]
daysAccurate=[]


for temp2 in asteet.find_all('td'):
    temperatures.append(temp2.text)
    
for time2 in kellonajat.find_all('td'):
    times.append(time2.text)
    
for day2 in paivat.find_all('td'):
    days.append(day2.text)

allInone=[]

    
def weather():
    lastTime=times[0]
    dayValue=0
    x=0
    xxx=0
    #infoDays={}
    todays=''
    for atTime in times:
        
        if int(lastTime[0])<=int(atTime[0]):
            daysAccurate.append(days[dayValue])
            if xxx==0:
                todays+='klo '+str(atTime)+' temp:'+str(temperatures[x])+'\n'
            #infoDays[days[dayValue]]=[atTime,temperatures[x]]
            
        else:
            
            # day has changed     
            if dayValue<len(days)-1:
                dayValue+=1
            #infoDays[days[dayValue]]=[atTime,temperatures[x]]
            daysAccurate.append(days[dayValue])
            xxx+=1
        x+=1
        lastTime=atTime
    
    allInone.append(daysAccurate)
    allInone.append(times)
    allInone.append(temperatures)
    allInone.append(todays)
    return allInone   














