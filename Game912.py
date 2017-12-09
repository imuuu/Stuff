import mysql.connector
from mysql.connector.errors import IntegrityError
import datetime
import random
import time
db = mysql.connector.connect(host="localhost",
                             user="dbuser",
                             passwd="dbpass",
                             db="whispertest",
                             buffered=True)

cur=db.cursor()

NewAreaDescription = [0,"You have arrived at some sort of village, there are multiple small buildings, but no-ones around", "area description","area description","You see a small church building nearby, it is in very poor condition."]
KnownAreaDescription = [0,"You arrive at some kind of small village, you have been here before ","area description", "area description", "You have returned to a familiar area, there is a small church building nearby"]
visitCounter = [0,0,0,0,0,0]


dt=datetime.datetime(1974,6,6,22,0)
square_side=50 #m
movement_multiplier=50
itemDropChange=0.5
enemySpawnRate=100 #%
#player max stats
player_carry_capasity=1500
player_max_healt=100
player_max_fatique=100
player_max_speed=15
player_max_attack=100

player_position_x=None
player_position_y=None
def help():
    print('''
HERE 
COMES 
COMMANDS
    
    
    
    ''')
def read(item):
    sql="SELECT item_type.name, item.id,item_type.id FROM item,item_type,player,terrain_square WHERE item.type_id=item_type.id and player.x=terrain_square.x and player.y=terrain_square.y and item.x=terrain_square.x and item.y=terrain_square.y"
    cur.execute(sql)
    result=cur.fetchall()
    for i in range(len(result)):
        if result[i][0].upper() == item:
            item_id=result[i][2]
    sql = "Select item_type.text FROM item_type, item where item_type.ID = item.type_id and item.type_ID='"+ str(item_id) +"'"
    cur.execute(sql)
    res = cur.fetchall()
    print(res)
    print(res[0][0])

def check_item_type(item):
    item=item.upper()
    sql = ("SELECT item_type.name FROM item_type WHERE item_type.name LIKE '"+item.lower()+"%'")
    
    cur.execute(sql)
    result = cur.fetchall()
    for i in range(len(result)):
        if result[i][0].upper() == item:
            return True
    
    return False      
def player_carry_att_speed_hp_fatique():
    sql=("SELECT player.carry,player.att,player.speed,player.hp,player.fatigue FROM player")
    cur.execute(sql)
    result=cur.fetchall()
    return result
def out_of_breath():
    potency = random.randrange(0, 15)
    multiplier = 0.98 ** potency
    return multiplier

def inventory():
    sql = "SELECT item_type.name, COUNT(*) FROM item,item_type WHERE item.type_id=item_type.id and item.player_ID>0 GROUP BY item_type.name"
    cur.execute(sql)
    result = cur.fetchall()
    sql=(("SELECT item_type.name,item_type.part FROM item,item_type WHERE item.type_id=item_type.id and item.equipped>0 GROUP BY item_type.name"))
    cur.execute(sql)
    result2=cur.fetchall()
    if (len(result))>0 or (len(result2))>0:
        if len(result)>0:
            print("==You are carrying==")
            for i in range(len(result)):
                print(("|"+result[i][0]+"(%s)")%(result[i][1]))
        if len(result2)>0:

            sql=(("SELECT item_type.name FROM item,item_type WHERE item.type_id=item_type.id and item.equipped>0 and item_type.part LIKE 'head%'"))
            cur.execute(sql)
            head=cur.fetchall()
            if len(head)>0:
                head=head[0][0]
            else:
                head=""
            sql=(("SELECT item_type.name FROM item,item_type WHERE item.type_id=item_type.id and item.equipped>0 and item_type.part LIKE 'body%'"))
            cur.execute(sql)
            body=cur.fetchall()
            if len(body)>0:
                body=body[0][0]
            else:
                body=""
            sql=(("SELECT item_type.name FROM item,item_type WHERE item.type_id=item_type.id and item.equipped>0 and item_type.part LIKE 'hand%'"))
            cur.execute(sql)
            hand=cur.fetchall()
            if len(hand)>0:
                hand=hand[0][0]
            else:
                hand=""
            sql=(("SELECT item_type.name FROM item,item_type WHERE item.type_id=item_type.id and item.equipped>0 and item_type.part LIKE 'leg%'"))
            cur.execute(sql)
            leg=cur.fetchall()
            if len(leg)>0:
                leg=leg[0][0]
            else:
                leg=""
            sql=(("SELECT item_type.name FROM item,item_type WHERE item.type_id=item_type.id and item.equipped>0 and item_type.part LIKE 'feet%'"))
            cur.execute(sql)
            feet=cur.fetchall()
            if len(feet)>0:
                feet=feet[0][0]
            else:
                feet=""
            print(''' ====Equipped====
|Head: %s     
|Body: %s   
|Hand: %s   
|Legs: %s
|Feet: %s   
================ 
            ''' % (head,body,hand,leg,feet))
            
    else:
        
        print("You don't carry any items with you")   
def add_time(distance,terrain_type_id):
    
    sql=("SELECT terrain_type.movement_difficulty FROM terrain_type WHERE terrain_type.id=%i" % terrain_type_id)
    cur.execute(sql)
    movement_dificulty=int(cur.fetchall()[0][0])
    
    sql=("SELECT player.speed FROM player")
    cur.execute(sql)
    speed=float(cur.fetchall()[0][0])
    #print(speed)
    multiplier=out_of_breath()
    x=speed*multiplier
    #print(x)
    time=int((distance/(x/(movement_multiplier*movement_dificulty))))
    tdelta=datetime.timedelta(seconds=time)
    global dt
    dt=(dt+tdelta)
    
def show_time():
    print(dt)
def update_player_weight(totalWeight):
    if totalWeight<=player_carry_capasity:
        sql=(("UPDATE player SET player.carry=%d WHERE player.ID=1") % totalWeight)
        cur.execute(sql)
    if totalWeight<0:
        sql=(("UPDATE player SET player.carry=0 WHERE player.ID=1"))
        cur.execute(sql)
def update_player_healt(totalHealt):
    if totalHealt<=player_max_healt and totalHealt>=0:
        sql=(("UPDATE player SET player.hp=%d WHERE player.ID=1") % totalHealt)
        cur.execute(sql)
    elif totalHealt<0:
        print("You lost the game!")
    else:
        sql=(("UPDATE player SET player.hp=%d WHERE player.ID=1") % player_max_healt)
        cur.execute(sql)
def update_player_fatique(totalFatique):
    if totalFatique<=player_max_fatique:
        sql=(("UPDATE player SET player.fatique=%d WHERE player.ID=1") % totalFatique)   
        cur.execute(sql)
def update_player_speed(totalSpeed):
    if totalSpeed<=player_max_speed:
        sql=(("UPDATE player SET player.speed=%d WHERE player.ID=1") % totalSpeed) 
        cur.execute(sql)
def update_player_attack(totalAttack):
    if totalAttack<=player_max_attack:
        sql=(("UPDATE player SET player.att=%d WHERE player.ID=1") % totalAttack)
        cur.execute(sql)
def drop_item(item):
    sql=("SELECT item_type.name,item.id FROM item,item_type WHERE item.type_id=item_type.id and item.player_ID>0")
    cur.execute(sql)
    result=cur.fetchall()
    for i in range(len(result)):
        if result[i][0].upper()==item:
            
            item_id=result[i][1]
            sql=("SELECT item_type.weight FROM item,item_type WHERE item.type_id=item_type.id and item.id=%i" % item_id)
            cur.execute(sql)
            item_weight=cur.fetchall()[0][0]
            
            totalWeight=((player_carry_att_speed_hp_fatique()[0][0])-item_weight)
            update_player_weight(totalWeight)
            
            pos=player_position()
            sql=("UPDATE item SET item.x=%i, item.y=%i, item.player_ID=NULL WHERE item.id=%i" % (pos[0][0],pos[0][1],item_id))
            cur.execute(sql)
            
            print("You dropped", result[i][0])
            break
        
def pick_up(item):
    
    sql="SELECT item_type.name, item.id FROM item,item_type,player,terrain_square WHERE item.type_id=item_type.id and player.x=terrain_square.x and player.y=terrain_square.y and item.x=terrain_square.x and item.y=terrain_square.y"
    cur.execute(sql)
    result=cur.fetchall()
    for i in range(len(result)):
        if result[i][0].upper()==item:
            item_id=result[i][1]
            
            sql=("SELECT item_type.weight FROM item,item_type WHERE item.type_id=item_type.id and item.id=%i" % item_id)
            cur.execute(sql)
            item_weight=cur.fetchall()[0][0]
            
            totalWeight=((player_carry_att_speed_hp_fatique()[0][0])+item_weight)
            if totalWeight<player_carry_capasity:
                sql=("UPDATE player SET player.carry=%d WHERE player.ID=1" % totalWeight)
                cur.execute(sql)
            
                sql=("UPDATE item SET item.x=NULL, item.y=NULL, item.player_ID=1 WHERE item.id=%i" % item_id)
                cur.execute(sql)
                print("You took", result[i][0])
            else:
                print("You cant get more weight to your poor back!")
            break

def player_position():
    sql="SELECT player.x,player.y FROM player"
    cur.execute(sql)
    result=cur.fetchall()
    return result
    
def split_line(text):
    words = text.split()
    return words

def look():
    sql ="Select terrain_type.name FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y+1"
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        print("North: " + res[0][0])
    sql ="Select terrain_type.name FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y-1"
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        print("South: " + res[0][0])
    sql ="Select terrain_type.name FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x+1"
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        print("East: " + res[0][0])
    sql ="Select terrain_type.name FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x-1"
    cur.execute(sql)
    res=cur.fetchall()
    if len(res)>0:
        print("West: " + res[0][0])
        
def move_north():
    global visitCounter
    
    sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res=cur.fetchall()
    oldAreaCode=res[0][2]
    if "S" in res[0][1]:
        print("You can't go through a wall, dummy")
    else:
        sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y+1"
        cur.execute(sql)
        res=cur.fetchall()
        newAreaCode = res[0][2]
        if len(res)>0:
            if res[0][0]==5:
                print("The forest is too thick, you cannot pass!")
            elif "N" in res[0][1]:
                print("You can't go through a wall, dummy")
            else:
                add_time(square_side, res[0][0])
                sql= "UPDATE player SET player.y = player.y +1"
                cur.execute(sql)
                sql="select terrain_type.name,terrain_square.area from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res=cur.fetchall()
                currentSquare = res[0][0]
                if newAreaCode != None and oldAreaCode != newAreaCode:
                    if visitCounter[newAreaCode]<1:
                        print(NewAreaDescription[newAreaCode])
                        visitCounter[newAreaCode]=1
                    else:
                        print(KnownAreaDescription[newAreaCode])
                print("You entered a " + currentSquare)
                enemySpawn()
        else:
            print("The ocean is that way,it would be suicide!")
            
def move_south():
    global visitCounter
    sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res=cur.fetchall()
    oldAreaCode = res[0][2]
    if "N" in res[0][1]:
        print("You can't go through a wall, dummy")
    else:
        sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y-1"
        cur.execute(sql)
        res=cur.fetchall()
        newAreaCode = res[0][2]
        if len(res)>0:
            if res[0][0]==5:
                print("The forest is too thick, you cannot pass!")
            elif "S" in res[0][1]:
                print("You can't go through a wall, dummy")
            else:
                add_time(square_side, res[0][0])
                sql= "UPDATE player SET player.y = player.y -1"
                cur.execute(sql)
                sql="select terrain_type.name from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res=cur.fetchall()
                currentSquare = res[0][0]
                if newAreaCode != None and oldAreaCode != newAreaCode:
                    if visitCounter[newAreaCode]<1:
                        print(NewAreaDescription[newAreaCode])
                        visitCounter[newAreaCode]=1
                    else:
                        print(KnownAreaDescription[newAreaCode])
                print("You entered a " + currentSquare)
                enemySpawn()
        else:
            print("The ocean is that way,it would be suicide!")
            
def move_east():
    global visitCounter
    sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res=cur.fetchall()
    oldAreaCode=res[0][2]
    if "W" in res[0][1]:
        print("You can't go through a wall, dummy")
    else:
        sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x+1"
        cur.execute(sql)
        res=cur.fetchall()
        newAreaCode = res[0][2]
        if len(res)>0:
            if res[0][0]==5:
                print("The forest is too thick, you cannot pass!")
            elif "E" in res[0][1]:
                print("You can't go through a wall, dummy")
            else:
                add_time(square_side, res[0][0])
                sql= "UPDATE player SET player.x = player.x +1"
                cur.execute(sql)
                sql="select terrain_type.name from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res=cur.fetchall()
                currentSquare = res[0][0]
                if newAreaCode != None and oldAreaCode != newAreaCode:
                    if visitCounter[newAreaCode]<1:
                        print(NewAreaDescription[newAreaCode])
                        visitCounter[newAreaCode]=1
                    else:
                        print(KnownAreaDescription[newAreaCode])
                print("You entered a " + currentSquare)
                enemySpawn()
        else:
            print("The ocean is that way,it would be suicide!")
            
def move_west():
    global visitCounter
    sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res=cur.fetchall()
    oldAreaCode=res[0][2]
    if "E" in res[0][1]:
        print("You can't go through a wall, dummy")
    else:
        sql ="Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x-1"
        cur.execute(sql)
        res=cur.fetchall()
        newAreaCode = res[0][2]
        if len(res)>0:
            if res[0][0]==5:
                print("The forest is too thick, you cannot pass!")
            elif "W" in res[0][1]:
                print("You can't go through a wall, dummy")
            else:
                add_time(square_side, res[0][0])
                sql= "UPDATE player SET player.x = player.x -1"
                cur.execute(sql)
                sql="select terrain_type.name from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res=cur.fetchall()
                currentSquare = res[0][0]
                if newAreaCode != None and oldAreaCode != newAreaCode:
                    if visitCounter[newAreaCode]<1:
                        print(NewAreaDescription[newAreaCode])
                        visitCounter[newAreaCode]=1
                    else:
                        print(KnownAreaDescription[newAreaCode])
                print("You entered a " + currentSquare)
                enemySpawn()        
        else:
            print("The ocean is that way,it would be suicide!")
def examine_area():
    sql=("SELECT item_type.name FROM item,item_type,player,terrain_square WHERE item.type_id=item_type.id and player.x=terrain_square.x and player.y=terrain_square.y and item.x=terrain_square.x and item.y=terrain_square.y")
    cur.execute(sql)
    result=cur.fetchall()
    if len(result)>0:
        print("You found the following items when searching the area ")
        for i in range(len(result)):
            print(result[i][0])
    else:
        print("There is nothing in this area")
def extended_look_desription(terrainTypeId,distance,frontTerraintypeId):
    x=random.randint(1,2)
    place=((distance*square_side)-(square_side/2))
    if terrainTypeId==0:
        if frontTerraintypeId==3:
            print("There is fall about %im away" % place)
        else:
            print("There is water about %im away" % (place))
    elif terrainTypeId==1:
        if x==1:
            print("ja noin %im paassa nakyy pienta avartunutta valoa" % (place))
        elif x==2:
            print("ja valo pilkistaa noin %im paasta" % (place))
    elif terrainTypeId==2:
        print("Forest starts about %im away" % (place))
    elif terrainTypeId==3:
        print("There is mountains about %im away" % place)
    elif terrainTypeId==4:
        if frontTerraintypeId==1:
            print("There starts beach about %im away" % place)
        else:
            print("There is something yellow on background about %im away" % (place))
    elif terrainTypeId==5:
        if frontTerraintypeId==2:
            print("Forest go thicker %im away" % place)
        else:
            print("There is starts thick Spruce Forest %im away" % place)
    elif terrainTypeId==10 or terrainTypeId==6 or terrainTypeId==7 or terrainTypeId==8 or terrainTypeId==9:
        print("There is some kind of large object blocking the view %im away" % place)
def extended_look(direction):
    getTerraintypeId=0
    distance=0
    if direction.upper()=="NORTH":
        
        sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y+1 and terrain_square.x=player.x")
        cur.execute(sql)
        result2=cur.fetchall()
        if len(result2)>0:
            for i in range(1,100):
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y+%i and terrain_square.x=player.x" % i)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    if i==1:
                        getTerraintypeId=result[0][0]
                    if getTerraintypeId==result[0][0]:
                        distance+=1
                    else:
                        break

            distance+=1       
            sql=("SELECT terrain_type.name FROM terrain_type WHERE terrain_type.id=%i" % getTerraintypeId)
            cur.execute(sql)
            result=cur.fetchall()
            lastResult=result
                
                
            if getTerraintypeId==1 or getTerraintypeId==2 or getTerraintypeId==3 or getTerraintypeId==4:
                print("Front of you there is",lastResult[0][0])
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y+%i and terrain_square.x=player.x" % distance)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    extended_look_desription(result[0][0],distance,lastResult[0][0])
                else:
                    extended_look_desription(0, distance,lastResult[0][0])
            else:
                print("There is %s blocking your vission" % result[0][0])
    if direction.upper()=="SOUTH":
        
        sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y-1 and terrain_square.x=player.x")
        cur.execute(sql)
        result2=cur.fetchall()
        if len(result2)>0:
            for i in range(1,100):
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y-%i and terrain_square.x=player.x" % i)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    if i==1:
                        getTerraintypeId=result[0][0]
                    if getTerraintypeId==result[0][0]:
                        distance+=1
                    else:
                        break

            distance+=1       
            sql=("SELECT terrain_type.name FROM terrain_type WHERE terrain_type.id=%i" % getTerraintypeId)
            cur.execute(sql)
            result=cur.fetchall()
            lastResult=result
                
                
            if getTerraintypeId==1 or getTerraintypeId==2 or getTerraintypeId==3 or getTerraintypeId==4:
                print("Front of you there is",lastResult[0][0])
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y-%i and terrain_square.x=player.x" % distance)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    extended_look_desription(result[0][0],distance,lastResult[0][0])
                else:
                    extended_look_desription(0, distance,lastResult[0][0])
            else:
                print("There is %s blocking your vission" % result[0][0])
    if direction.upper()=="WEST":
        
        sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x-1")
        cur.execute(sql)
        result2=cur.fetchall()
        if len(result2)>0:
            for i in range(1,100):
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x-%i" % i)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    if i==1:
                        getTerraintypeId=result[0][0]
                    if getTerraintypeId==result[0][0]:
                        distance+=1
                    else:
                        break

            distance+=1       
            sql=("SELECT terrain_type.name FROM terrain_type WHERE terrain_type.id=%i" % getTerraintypeId)
            cur.execute(sql)
            result=cur.fetchall()
            lastResult=result
                
                
            if getTerraintypeId==1 or getTerraintypeId==2 or getTerraintypeId==3 or getTerraintypeId==4:
                print("Front of you there is",lastResult[0][0])
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x-%i" % distance)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    extended_look_desription(result[0][0],distance,lastResult[0][0])
                else:
                    extended_look_desription(0, distance,lastResult[0][0])
            else:
                print("There is %s blocking your vission" % result[0][0])
    if direction.upper()=="EAST":
        
        sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x+1")
        cur.execute(sql)
        result2=cur.fetchall()
        if len(result2)>0:
            for i in range(1,100):
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x+%i" % i)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    if i==1:
                        getTerraintypeId=result[0][0]
                    if getTerraintypeId==result[0][0]:
                        distance+=1
                    else:
                        break

            distance+=1       
            sql=("SELECT terrain_type.name FROM terrain_type WHERE terrain_type.id=%i" % getTerraintypeId)
            cur.execute(sql)
            result=cur.fetchall()
            lastResult=result
                
                
            if getTerraintypeId==1 or getTerraintypeId==2 or getTerraintypeId==3 or getTerraintypeId==4:
                print("Front of you there is",lastResult[0][0])
                sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x+%i" % distance)
                cur.execute(sql)
                result=cur.fetchall()
                if len(result)>0:
                    extended_look_desription(result[0][0],distance,lastResult[0][0])
                else:
                    extended_look_desription(0, distance,lastResult[0][0])
            else:
                print("There is %s blocking your vission" % result[0][0])
def player_stats():
    sql=("SELECT player.carry, player.att,player.speed,player.hp,player.fatigue FROM player")
    cur.execute(sql)
    result=cur.fetchall()
    print(('''
==============
|Healt    %s     
|Carrying %s   
|Attack   %s   
|Fatiogue %s
|Speed    %s   
==============   
    ''') % (result[0][3],result[0][0],result[0][1],result[0][4],result[0][2]))
def eat(foodName):
    sql=(("SELECT item_type.name,item.id,item_type.healing,item_type.weight, COUNT(*) FROM item,item_type WHERE item.type_id=item_type.id and item.player_ID>0 and item_type.name LIKE '"+foodName.lower()+"%' GROUP BY item_type.name"))
    cur.execute(sql)
    result=cur.fetchall()
    if len(result)>0:
        if result[0][2]!=0:
            itemID=result[0][1]
            
            itemHealing=result[0][2]
            totalHealt=((player_carry_att_speed_hp_fatique()[0][3])+itemHealing)
            update_player_healt(totalHealt)
            
            item_weight=result[0][3]
            totalWeight=((player_carry_att_speed_hp_fatique()[0][0])-item_weight)
            update_player_weight(totalWeight)
            
            sql=(("DELETE FROM item WHERE item.id=%i") % itemID)
            cur.execute(sql)
        else:
            print("You can't eat %s or do you have metal teeth or something?" % result[0][0])
    else:
        print(("You don't have item called %s in your inventory") % (foodName.lower()))
def sleep(hours):
    global dt
    if hours>12:
        hours=12
    if hours<0:
        hours=0
    itemIshere=0
    sql=(("SELECT item_type.id,item_type.name  FROM item,item_type,player,terrain_square WHERE item.type_id=item_type.id and player.x=terrain_square.x and player.y=terrain_square.y and item.x=terrain_square.x and item.y=terrain_square.y"))
    cur.execute(sql)
    itemsIdsINarea=cur.fetchall()
    checkItemsId=[41,42]
    sql=(("Select terrain_type.Id,terrain_square.restriction,terrain_square.area FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"))
    cur.execute(sql)
    terrainTypeId=cur.fetchall()
    
    if (terrainTypeId[0][0])==10 or (terrainTypeId[0][0])==6 or (terrainTypeId[0][0])==7 or (terrainTypeId[0][0])==8 or (terrainTypeId[0][0])==9:
        for i in range(len(itemsIdsINarea)):
            for x in range(len(checkItemsId)):
                if (itemsIdsINarea[i][0])==checkItemsId[x]:
                    itemIshere=1
                    if dt.hour>=22 and dt.hour<=23 or dt.hour>=0 and dt.hour<=8:
                        
                        time=(60*60*hours)
                        tdelta=datetime.timedelta(seconds=time)
                    
                        dt=(dt+tdelta)
                        print("You slept %ih and time is now %s" % (hours,dt))
                        break
                    else:
                        print("You can't sleep now there is still light")
                        break
        if itemIshere==0:
            print("There is nothing where you can lay on")
    else:
        print("Here is not safe to sleep")       

def combineITEMS(itemId1,itemId2):
    itemids=[itemId1,itemId2]
    itemids.sort()
    #item1=0
    #item2=0
    #combineItems=[58,10,37,38,57]
    searchProduct={(37,38):39,(57,58):36,(9,58):80,(38,80):81,(31,58):76,(38,50):82,(19,38):83,(20,38):84,(22,38):85,(6,10):86,(10,58):87,(13,93):94,(13,95):96}
    #39 poison arrow
    #36 bow
    #80 spear
    #81 toxic spear
    #76 slingshot
    #82 toxic axe
    #83 poisoned blade
    #84 poisoned shovel
    #85 poisoned rake
    #86 paperweight
    
    #85 stone spear
    #94 spiked baton
    #96 spiked baseball bat
    try:
        productId=searchProduct[itemids[0],itemids[1]]
        return productId
    except:
        return False
        
    return False
def combine(twoItems):
    print(twoItems)
    itemnames=[]
    for i in range(len(twoItems)):
        itemnames.append(twoItems[i].lower())
    print(itemnames)
    if (check_item_type(itemnames[0]))==True and (check_item_type(itemnames[1]))==True:
        
        sql=(("SELECT item_type.name,item_type.id FROM item_type,item WHERE item.type_id=item_type.id and item.player_ID>0 and item_type.name like '"+itemnames[0]+"%'"))
        cur.execute(sql)
        item1=cur.fetchall()
        sql=(("SELECT item_type.name,item_type.id FROM item_type,item WHERE item.type_id=item_type.id and item.player_ID>0 and item_type.name like '"+itemnames[1]+"%'"))
        cur.execute(sql)
        item2=cur.fetchall()
        #print(item1[0][1])
        totalLen=(len(item1)+len(item2))
        if totalLen>1:
            try:
                productId=combineITEMS(item1[0][1], item2[0][1])
            except:
                print("You need to have both items in your inventory to able to craft")
                productId=0
            if productId>0:
                sql=("SELECT MAX(item.id) FROM item")
                cur.execute(sql)
                maxId=cur.fetchall()[0][0]
                newItemsID=(maxId+1)
                sql=(("SELECT item_type.name,item_type.weight FROM item_type WHERE item_type.id=%i") % productId)
                cur.execute(sql)
                result=cur.fetchall()
                newItemsName=result[0][0]
                #new Item made for player inv(below)
                sql=(("INSERT INTO item VALUES (%i,%i,0,0,1)") % (newItemsID,productId))
                cur.execute(sql)
                
                sql=(("SELECT item.id,item_type.name,item_type.weight FROM item,item_type WHERE item.type_id=item_type.id and item_type.name like '"+itemnames[0]+"%' and item.player_ID>0"))
                cur.execute(sql)
                fItemID=cur.fetchall()
                sql=(("SELECT item.id,item_type.name,item_type.weight FROM item,item_type WHERE item.type_id=item_type.id and item_type.name like '"+itemnames[1]+"%' and item.player_ID>0"))
                cur.execute(sql)
                sItemID=cur.fetchall()
                
                sql=(("DELETE FROM item WHERE item.id=%i")% (fItemID[0][0]))
                cur.execute(sql)
                sql=(("DELETE FROM item WHERE item.id=%i")% (sItemID[0][0]))
                cur.execute(sql)
                
                totalWeight=(((player_carry_att_speed_hp_fatique()[0][0])-(fItemID[0][2]+sItemID[0][2]))+result[0][1])
                print(totalWeight)
                update_player_weight(totalWeight)
                
                print("You crafted",newItemsName)
        else:
            print("You need to have both items in your inventory to able to craft")
    else:
        print("There isn's such a item(s)")    
def equip(item):
    item=item.lower()
    sql=(("SELECT item.id,item_type.name,item_type.att,item_type.defense,item.type_id,item_type.part FROM item, item_type WHERE item.type_id=item_type.id and item.player_ID>0 and item_type.name LIKE '"+item+"%'"))
    #print(sql)
    cur.execute(sql)
    itemINFO=cur.fetchall()
    
    if len(itemINFO)>0:
        itemTypeID=itemINFO[0][4]
        itemID=itemINFO[0][0]
        itemName=itemINFO[0][1]
        itemAtt=itemINFO[0][2]
        itemDEFF=itemINFO[0][3]
        itemPart=itemINFO[0][5]
        
        if itemPart=="feet" or itemPart=="leg" or itemPart=="body" or itemPart=="head" or itemPart=="hand" or itemAtt>0 or itemDEFF>0:
            sql=(("SELECT item_type.name FROM item, item_type WHERE item.type_id=item_type.id and item.equipped=1 and item_type.part like '"+itemPart+"%'"))
            #print(sql)
            cur.execute(sql)
            eqPart=cur.fetchall()
            if len(eqPart)<1:
                sql=(("UPDATE item SET item.player_ID=NULL, item.equipped=1 WHERE item.id=%i") % itemID)
                cur.execute(sql)
                
                totalHP=(player_carry_att_speed_hp_fatique()[0][3]+itemDEFF)
                global player_max_healt
                player_max_healt+=itemDEFF
                update_player_healt(totalHP)
                
                totalAtt=(player_carry_att_speed_hp_fatique()[0][1]+itemAtt)
                update_player_attack(totalAtt)
                print("You have just equipped",itemName)
                
            else:
                print("You have equipment in that slot already")
        else:
            print("You can't equip that")
    else:
        print("You don't have item in your inventory") 
def unEquip(item):
    item=item.lower()
    sql=(("SELECT item.id,item_type.name,item_type.att,item_type.defense,item.type_id,item_type.part FROM item, item_type WHERE item.type_id=item_type.id and item.equipped=1 and item_type.name like '"+item+"%'"))
    cur.execute(sql)
    itemINFO=cur.fetchall()
    
    if len(itemINFO)>0:
        itemTypeID=itemINFO[0][4]
        itemID=itemINFO[0][0]
        itemName=itemINFO[0][1]
        itemAtt=itemINFO[0][2]
        itemDEFF=itemINFO[0][3]
        itemPart=itemINFO[0][5]
        
        sql=(("UPDATE item SET item.player_ID=1, item.equipped=NULL WHERE item.id=%i") % itemID)
        cur.execute(sql)
        
        totalHP=(player_carry_att_speed_hp_fatique()[0][3]-itemDEFF)
        global player_max_healt
        
        if totalHP<1:
            update_player_healt(1)
        else:
            update_player_healt(totalHP)
        player_max_healt-=itemDEFF
        totalAtt=(player_carry_att_speed_hp_fatique()[0][1]-itemAtt)
        update_player_attack(totalAtt)
        print("You have just unequipped",itemName)
        
    else:
        print("You don't have that item equipped")
def randomItemDrops():
    trashItemIds=[58,86,38,17,13,11,10,4,3,2,1,89]
    commonItemIds=[8,67,12,57,48,35,31,88,91,72,69,34,98,99,106,107,109,110,111]
    rareItemIds=[6,9,71,47,44,37,76,22,20,50,5,92,93,95,103,105,108]
    legendaryItemIds=[25,19,9,90,49,42,97,100,101,102,104]
    
def combat(enemyName):
    enemyName=enemyName.lower()
    sql=(("SELECT enemy.id,enemy_type.id, enemy_type.name,enemy_type.hp,enemy_type.att,enemy_type.speed,enemy_type.description, enemy_type.description2,enemy_type.seen FROM enemy,enemy_type,player,terrain_square WHERE enemy.type_id=enemy_type.id and player.x=terrain_square.x and player.y=terrain_square.y and enemy.x=terrain_square.x and enemy.y=terrain_square.y and enemy_type.name='%s'")% (enemyName))    
    cur.execute(sql)
    enemyINFO=cur.fetchall()
    if len(enemyINFO)>0:
        print("Attack is starting...")
        enemyTypeID=enemyINFO[0][1]
        enemyID=enemyINFO[0][0]
        enemyName=enemyINFO[0][2]
        enemyHP=enemyINFO[0][3]
        enemyAtt=enemyINFO[0][4]
        enemySpeed=enemyINFO[0][5]
        
        playerHP=player_carry_att_speed_hp_fatique()[0][0]
        playerAtt=player_carry_att_speed_hp_fatique()[0][0]
        playerSpeed=player_carry_att_speed_hp_fatique()[0][0]
        
        x="."
        for i in range(1,4):
            time.sleep(1.5)
            print(x*i)
        print("You are in combat with",enemyName)
        if playerSpeed<enemySpeed:
            print("and you were faster than enemy, you hit",enemyName)
            enemyHP-=playerAtt
        else:
            print("and got hit by it")
            playerHP-=enemyAtt
        for i in range(1,4):
            time.sleep(1)
            print(x*i)
        human='''             x====x
             |head|            
        x====x====x====x
        |hand|body|hand|            
        x====x====x====x     
             |legs|       
             x====x
             |feet|
             x====x    '''
        handlesshuman='''             x====x
             |head|            
             x====x
             |body|            
             x====x     
             |legs|       
             x====x
             |feet|
             x====x    '''
        leglesshuman='''             x====x
             |head|            
        x====x====x====x
        |hand|body|hand|            
        x====x====x====x     
             ||||||    '''
        fourlegs='''       xx====x====x====x====x
      x |====|body|====|head|
     x  x====x====x====x====x
        |legs||   |legs||
        x====xx   x====xx
        '''
        bird='''             x====x
             |head|            
             x====x
            x|body|x            
           x x====x x    
             |legs|       
             x====x
                    '''
        xx=0
        while playerHP>0 or enemyHP>0:
            if xx==0:
                print("\n"*100)
                xx=1
            else:
                x="."
                for i in range(1,5):
                    time.sleep(0.5)
                    print(x*i)
                print("\n"*100)
            
            print("\t    Healt:%i"%enemyHP)
            if enemyTypeID in [1,2]:
                print(human)
                hitlist=["head","hand","body","legs","feet"]
            elif enemyTypeID==4:
                print(handlesshuman)
                hitlist=["head","body","legs","feet"]
            elif enemyTypeID==3:
                print(leglesshuman)
                hitlist=["head","hand","body"]
            elif enemyTypeID in [5,6,7,8,9]:
                print(fourlegs)
                hitlist=["head","body","legs","feet"]
            elif enemyTypeID==10:
                print(bird)
                hitlist=["head","body","legs"]
            print()
            print("You are combat with",enemyName)
            playerINPUT=input("Where you wanna hit: ")
            playerINPUT.lower()
            if playerINPUT in hitlist:
                print("hitting...")
            else:
                print("you didnt hit")
        
        
    else:   
        print("There isn't that kind of character in area")
def enemySpawn():
    
   
    neutralEnemiesIds=[5,8,10]
    sql=(("SELECT enemy.id,enemy_type.id, enemy_type.name,enemy_type.hp,enemy_type.att,enemy_type.speed, terrain_square.type_id, enemy_type.description, enemy_type.description2,enemy_type.seen FROM enemy,enemy_type,player,terrain_square WHERE enemy.type_id=enemy_type.id and player.x=terrain_square.x and player.y=terrain_square.y and enemy.x=terrain_square.x and enemy.y=terrain_square.y"))    
    cur.execute(sql)
    enemies=cur.fetchall()
    
    sql=("SELECT terrain_type.Id FROM terrain_type,terrain_square,player WHERE terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x")
    cur.execute(sql)
    result=cur.fetchall()
    
    if len(enemies)>1: #delete all other enemies expect one
        for i in range(len(enemies)-1):
            id=enemies[(i+1)][0]
            sql=("DELETE FROM enemy WHERE id=%i" % id)
            cur.execute(sql)
    
    elif len(enemies)<1 and (result[0][0]) in [1,2,3,4]:
        sql=("SELECT MAX(enemy.id) FROM enemy")
        cur.execute(sql)
        newId=(cur.fetchall()[0][0]+1)
        spawn=random.randint(1,100)
        enemyTypeId=random.randint(1,10)
        
        if spawn<=enemySpawnRate:
            playerPOS=player_position()
            sql=("INSERT INTO enemy VALUES (%i,%i,%i,%i)" % (newId,enemyTypeId,playerPOS[0][0],playerPOS[0][1]) )
            cur.execute(sql)
    
    distanceBetweenYou=random.randint(7,square_side+7)
    sql=(("SELECT enemy.id,enemy_type.id, enemy_type.name,enemy_type.hp,enemy_type.att,enemy_type.speed, terrain_square.type_id, enemy_type.description, enemy_type.description2,enemy_type.seen FROM enemy,enemy_type,player,terrain_square WHERE enemy.type_id=enemy_type.id and player.x=terrain_square.x and player.y=terrain_square.y and enemy.x=terrain_square.x and enemy.y=terrain_square.y"))    
    cur.execute(sql)
    enemies=cur.fetchall()
   
    
    if len(enemies)>0:
        seen=enemies[0][9]
        sql=("UPDATE enemy_type SET seen=1 WHERE id=%i" % enemies[0][1])
        cur.execute(sql)
        #print(enemies)     
        
        timeToReachPlayer=distanceBetweenYou/(enemies[0][5]) #seconds
        
        if (enemies[0][1]) in neutralEnemiesIds:
            action=random.randint(1,3)
            if action==1:
                print("There is "+enemies[0][2]+" passing you")
            elif action==2:
                if (enemies[0][1])!=10:
                    print(enemies[0][2]+" is running away from you")
                else:
                    print(enemies[0][2]+" is flying past you")
            else:
                print(enemies[0][2]+" is standing still and looking at you")
            
        else:
            print(str(timeToReachPlayer)+"s")
            print(str(distanceBetweenYou)+"m")
            
            if distanceBetweenYou<=15:
                if seen>0:
                    print(enemies[0][2]+" sees you")
                else:
                    print(str(enemies[0][7])+" sees you")
                if timeToReachPlayer<=10:
                    if (enemies[0][1])!=3:
                        xxx=1
                        print("it is running towards you aggressively, you don't have time to react")
                    else:
                        xxx=random.randint(1,2)
                        print("it is crawling towards you aggressively, you don't have time to react")
                    if enemies[0][1]==3 and xxx==2:
                        x="."
                        for i in range(1,4):
                            time.sleep(1)
                            print(x*i)
                        print("but thank god this creature fell to hole next to it")
                    else:   
                        combat(enemies[0][2])
                else:
                    #print("but it is moving slowly towards you, and you estimate its gonna reach you in about %is" % (int(timeToReachPlayer)+3))
                    print("but it is moving too slow")
                          
            else:
                if seen>0:
                    print(enemies[0][2]+" is too far away from you to see")
                else:
                    print(str(enemies[0][7])+" is too far away from you to see")
    else:
        print("No enemy")
  
def parse(playerInput):

    playerCaps = playerInput.upper()
    filter = [".", ",",":"," an "," a ","move ", "go ", " in ", " out ", " the ", " and "]
    filteredText = ''.join([c for c in playerCaps if c not in filter])
    playerText = split_line(filteredText)
    #print(playerText)
    if len(playerText)<1:
        print("Are you an empty vessel?")
    elif playerText[0]== "N" or playerText[0]=="NORTH":
        move_north()
    elif (playerText[0])== "S" or playerText[0]=="SOUTH":
        move_south()
    elif (playerText[0])== "W" or playerText[0]=="WEST":
        move_west()
    elif (playerText[0])== "E" or playerText[0]=="EAST":
        move_east()
    elif (playerText[0])== "LOOK" or playerText[0]=="L" or playerText[0]=="WATCH" or playerText[0]=="SEE":
        if len(playerText)>1:
            if (playerText[0])=="LOOK" and (playerText[1])=="NORTH" or (playerText[1])=="SOUTH" or (playerText[1])=="WEST" or (playerText[1])=="EAST":
                extended_look(playerText[1])
        else:
            look()
    elif (playerText[0])=="I":
        inventory()
    
    elif (playerText[0])=="DROP":
        item=""
        for i in range(len(playerText)):
            if i>=1:
                if i<(len(playerText)-1):
                    item+=(playerText[i]+" ")
                else:
                    item+=(playerText[i])
        drop_item(item)
    elif (playerText[0])=="COMBINE":
        if len(playerText)>1:
            item=""
            for i in range(len(playerText)):
                if i>=1:
                    if i<(len(playerText)-1):
                        item+=(playerText[i]+" ")
                    else:
                        item+=(playerText[i])
            pos=item.find("+")
            if item[(pos-1)]==" " and item[(pos+1)]==" ":
                newitem=item[:(pos-1)]+item[pos:]
                print("newitem",newitem)
                newitem2=newitem[:(pos)]+newitem[(pos+1):]
            
            elif item[(pos-1)]==" " and item[(pos+1)]!=" ":
                newitem=item[:(pos-1)]+item[pos:]
                print("newitem",newitem)
                newitem2=newitem[:(pos)]+newitem[(pos):]
            
            elif item[(pos-1)]!=" " and item[(pos+1)]==" ":
                newitem=item[:(pos)]+item[pos:]
                print("newitem",newitem)
                newitem2=newitem[:(pos+1)]+newitem[(pos+2):]
            else:
                newitem2=item
            
            pos2=newitem2.find("+")    
            item1=newitem2[0:pos2]
            item2=newitem2[(pos2+1):len(newitem2)]
            
            list=[item1,item2]
            combine(list)
        else:
            print("You ment? combine item+item")    
    elif (playerText[0])=="TIME":
        show_time()
    elif (playerText[0])== "KILL" or "ATTACK" or "ENGAGE" or "FIGHT" or "BATTLE":
        item=""
        if len(playerText)>1:
            for i in range(len(playerText)):
                if i>=1:
                    if i<(len(playerText)-1):
                        item+=(playerText[i]+" ")
                    else:
                        item+=(playerText[i])
            
            combat(item)
        else:
            print("You meant attack enemy?")
    elif (playerText[0])=="EQUIP":
        item=""
        if len(playerText)>1:
            for i in range(len(playerText)):
                if i>=1:
                    if i<(len(playerText)-1):
                        item+=(playerText[i]+" ")
                    else:
                        item+=(playerText[i])
            equip(item)
        else:
            print("You meant equip item?")
    elif (playerText[0])=="UNEQUIP":
        item=""
        if len(playerText)>1:
            for i in range(len(playerText)):
                if i>=1:
                    if i<(len(playerText)-1):
                        item+=(playerText[i]+" ")
                    else:
                        item+=(playerText[i])
            unEquip(item)
        else:
            print("You meant unequip item?")
        
    elif (playerText[0])== "EXAMINE":
        if len(playerText)>1:
            if(playerText[1])== "AREA":
                    examine_area()
    elif (playerText[0])=="STATS":
        player_stats()
    elif (playerText[0])=="HELP":
        help()
    elif (playerText[0])=="EAT":
        item=""
        if len(playerText)>1:
            for i in range(len(playerText)):
                if i>=1:
                    if i<(len(playerText)-1):
                        item+=(playerText[i]+" ")
                    else:
                        item+=(playerText[i])
            eat(item)
        else:
            print("You ment? eat 'name of item'")
    elif (playerText[0])=="SLEEP":
        if len(playerText)>1:
            
            sleep(int(playerText[1]))
        else:
            sleep(6)
    elif (playerText[0]) == "TAKE" or "PICK" or "PICKUP" or "GRAB":
        item=""
        if len(playerText)>1:
            if(playerText[1]) == "UP" and playerText[0] == "PICK":
                for i in range(len(playerText)):
                    if i>=2:
                        if i<(len(playerText)-1):
                            item+=(playerText[i]+" ")
                        else:
                            item+=(playerText[i])
                
                if check_item_type(item)==True:
                    pick_up(item)
                else:
                    print("There isn's such a item")
            else:
                for i in range(len(playerText)):
                    if i>=1:
                        if i<(len(playerText)-1):
                            item+=(playerText[i]+" ")
                        else:
                            item+=(playerText[i])
                
                if check_item_type(item)==True:
                    pick_up(item)
    
        #actions
    #elif (playerText[0])== "I" or "INVENTORY" or "BAG" or "ITEMS":
        #display inventory
    
    #elif (playerText[0])== "EXAMINE" or "INSPECT" or "STUDY" or "ANALYZE":
        #display info of enemy in the map
    elif (playerText[0])== "READ":
        item=""
        for i in range(1,len(playerText)):
            if i<(len(playerText)-1):
                item+=(playerText[i]+" ")
            else:
                item+=(playerText[i])
        print(item)
        if check_item_type(item)==True:
            read(item)
    #elif (playerText[0])== "S" or "SOUTH":
        #actions
    #elif (playerText[0])== "S" or "SOUTH":
        #actions

def main():
    update_player_healt(4)
    while True:
        
        
        
        
        
        
        #player_stats()
        #out_of_breath()
        #print(player_carry())
        
        #print(player_carry_att_speed_hp_fatique()[0][1])
        #eat("backpack")
        print(player_position())
        playerInput = input()
        parse(playerInput)
        
    
main()