import random

lottoNumbers = []
ticket = []
numbers = 7
between1 = 1
between2 = 40

keepSameTicket=1
hitss=6

def checkInlist(number,list):
    if number not in list:
        return False
        print("not")
    else:
        return True
        print("yes")
def randomNumber():
    randNumber=random.randint(between1,between2)
    return randNumber
def weekLottoNumbers():
    xxx=True

    while xxx==True:
        num=randomNumber()

        if checkInlist(num,lottoNumbers)== False:
            lottoNumbers.append(num)
        if len(lottoNumbers)>=numbers:
            lottoNumbers.sort()
            print("Week Numbers are:",lottoNumbers)
            xxx=False
def yourTicket():
    xxx=True

    while xxx==True:
        num=randomNumber()

        if checkInlist(num,ticket)== False:
            ticket.append(num)
        if len(ticket)>=numbers:
            ticket.sort()
            print("Your Numbers are:",ticket)
            xxx=False
def howManyHits():
    hits=0
    hitss=[]
    for i in range(len(ticket)):
        if ticket[i] in lottoNumbers:
            hits+=1
            hitss.append((ticket[i]))

    if len(hitss)>0:
        print(hitss)
    print("You got %i hits" % hits)

    return hits
def weekTotimes(week):

    days=week*7
    hours=days*24
    minutes=hours*60
    seconds=minutes*60
    months = week / 4
    years = months / 12

    print("Years:",years)
    print("Months:",months)
    print("Days:",days)
    print("Hours:",hours)
    print("Minutes:",minutes)
    print("Seconds:",seconds)
def main():
    weeks=0
    days=0
    hours=0
    minutes=0

    won=False
    hitsToWin=len(ticket)
    if hitss>0:
        hitsToWin=hitss
    while won==False:
        try:
            print(weeks)
            weekTotimes(weeks)
            if keepSameTicket==1:
                if len(ticket)<=0:
                    yourTicket()
                else:
                    print("Your Numbers are:", ticket)
            else:
                yourTicket()
            weekLottoNumbers()



            weeks+=1
            if howManyHits()==hitsToWin:
                won=True
            if keepSameTicket==0:
                ticket.clear()
            lottoNumbers.clear()
        except KeyboardInterrupt:
            break

    print(len(ticket))

main()
