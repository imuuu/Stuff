def split_line(text):
    words = text.split()
    return words
playerInput=input()
playerCaps = playerInput.upper()
filter = [".", ",",":"," an "," a ","move ", "go ", " in ", " out ", " the ", " and "]
filteredText = ''.join([c for c in playerCaps if c not in filter])
playerText = split_line(filteredText)



print(playerText[1])
print(playerText[2])

print(playerText[1]+" "+playerText[2])
item=(playerText[1]+" "+playerText[2])
print(playerText[1:5])
item2=playerText[1:5]
print(item)
print(item2)

test=playerText[1]
test2=playerText[2]
test3=playerText[3]

tess=test+test2

print(tess)
tess+=test3
print(tess)
tess2=""
for i in range(len(playerText)):
    
    if i>=1:
        tess2+=(playerText[i]+" ")
print(tess2)