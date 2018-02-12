import random
lottoNumbers=[]
ticker=[]
numbers=7
between1=1
between2=40

for i in range(1,numbers+1):
    randNumber=random.randint(between1, between2)
    if randNumber not in lottoNumbers:
        lottoNumbers.append(randNumber)
        print("NOP")
    else:
        numbers+=1
        print("yes")
    
    print(randNumber)
print(lottoNumbers)
    
    