import mysql.connector
from mysql.connector.errors import IntegrityError
import datetime
import random
db = mysql.connector.connect(host="localhost",
                             user="dbuser",
                             passwd="dbpass",
                             db="whispertest",
                             buffered=True)

cur = db.cursor()

player_carry_capasity = 150
dt = datetime.datetime(1974, 6, 6, 9, 0)
square_side = 50  # m
movement_multiplier = 50
def check_item_type(item):
    sql = ("SELECT item_type.name FROM item_type")
    cur.execute(sql)
    result = cur.fetchall()
    marks=0
    for i in range(len(result)):
        if result[i][0].upper() == item:
            
            return True
            
    return False      
def player_carry():
    sql = ("SELECT player.carry FROM player")
    cur.execute(sql)
    result = cur.fetchall()[0][0]
    return result
def out_of_breath():
    potency = random.randrange(0, 15)
    multiplier = 0.98 ** potency
    return multiplier

def inventory():
    sql = "SELECT item_type.name FROM item,item_type WHERE item.type_id=item_type.id and item.player_ID>0"
    cur.execute(sql)
    result = cur.fetchall()
    
    # print("You have %d items in your inventory" % (len(result)))
    print("Your items(%d) are following: " % (len(result)))
    for i in range(len(result)):
        print(result[i][0])
def add_time(distance, terrain_type_id):
    
    sql = ("SELECT terrain_type.movement_difficulty FROM terrain_type WHERE terrain_type.id=%i" % terrain_type_id)
    cur.execute(sql)
    movement_dificulty = int(cur.fetchall()[0][0])
    
    sql = ("SELECT player.speed FROM player")
    cur.execute(sql)
    speed = float(cur.fetchall()[0][0])
    
    multiplier = out_of_breath()
    x = speed * multiplier
    
    time = int((distance / (x / (movement_multiplier * movement_dificulty))))
    tdelta = datetime.timedelta(seconds=time)
    global dt
    dt = (dt + tdelta)
    
def show_time():
    print(dt)
    
def drop_item(item):
    sql = ("SELECT item_type.name,item.id FROM item,item_type WHERE item.type_id=item_type.id and item.player_ID>0")
    cur.execute(sql)
    result = cur.fetchall()
    for i in range(len(result)):
        if result[i][0].upper() == item:
            
            item_id = result[i][1]
            sql = ("SELECT item_type.weight FROM item,item_type WHERE item.type_id=item_type.id and item.id=%i" % item_id)
            cur.execute(sql)
            item_weight = cur.fetchall()[0][0]
            
            totalWeight = (player_carry() - item_weight)
            sql = ("UPDATE player SET player.carry=%d WHERE player.ID=1" % totalWeight)
            cur.execute(sql)
            
            pos = player_position()
            sql = ("UPDATE item SET item.x=%i, item.y=%i, item.player_ID=NULL WHERE item.id=%i" % (pos[0][0], pos[0][1], item_id))
            cur.execute(sql)
            
            print("You dropped", result[i][0])
            break
    
def pick_up(item):
    
    sql = "SELECT item_type.name, item.id FROM item,item_type,player,terrain_square WHERE item.type_id=item_type.id and player.x=terrain_square.x and player.y=terrain_square.y and item.x=terrain_square.x and item.y=terrain_square.y"
    cur.execute(sql)
    result = cur.fetchall()
    for i in range(len(result)):
        if result[i][0].upper() == item:
            item_id = result[i][1]
            
            sql = ("SELECT item_type.weight FROM item,item_type WHERE item.type_id=item_type.id and item.id=%i" % item_id)
            cur.execute(sql)
            item_weight = cur.fetchall()[0][0]
            
            totalWeight = (player_carry() + item_weight)
            if totalWeight < player_carry_capasity:
                sql = ("UPDATE player SET player.carry=%d WHERE player.ID=1" % totalWeight)
                cur.execute(sql)
            
                sql = ("UPDATE item SET item.x=NULL, item.y=NULL, item.player_ID=1 WHERE item.id=%i" % item_id)
                cur.execute(sql)
                print("You took", result[i][0])
            else:
                print("You cant get more weight to your poor back!")
            break

def player_position():
    sql = "SELECT player.x,player.y FROM player"
    cur.execute(sql)
    result = cur.fetchall()
    return result
    
def split_line(text):
    words = text.split()
    return words

def look():
    sql = "Select terrain_type.name FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y+1"
    cur.execute(sql)
    res = cur.fetchall()
    if len(res) > 0:
        print("North: " + res[0][0])
    sql = "Select terrain_type.name FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y-1"
    cur.execute(sql)
    res = cur.fetchall()
    if len(res) > 0:
        print("South: " + res[0][0])
    sql = "Select terrain_type.name FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x+1"
    cur.execute(sql)
    res = cur.fetchall()
    if len(res) > 0:
        print("East: " + res[0][0])
    sql = "Select terrain_type.name FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x-1"
    cur.execute(sql)
    res = cur.fetchall()
    if len(res) > 0:
        print("West: " + res[0][0])
        
def move_north():
    
    sql = "Select terrain_type.Id,terrain_square.restriction FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res = cur.fetchall()
    if "S" in res[0][1]:
        print("You can't go through a wall, dummy")
    else:
        sql = "Select terrain_type.Id,terrain_square.restriction FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y+1"
        cur.execute(sql)
        res = cur.fetchall()
        print(res)
        if len(res) > 0:
            if res[0][0] == 5:
                print("The forest is too thick, you cannot pass!")
            elif "N" in res[0][1]:
                print("You can't go through a wall, dummy")
            else:
                add_time(square_side, res[0][0])
                sql = "UPDATE player SET player.y = player.y +1"
                cur.execute(sql)
                sql = "select terrain_type.name from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res = cur.fetchall()
                currentSquare = res[0][0]
                print("You entered a " + currentSquare)
        else:
            print("The ocean is that way,it would be suicide!")
            
def move_south():
    sql = "Select terrain_type.Id,terrain_square.restriction FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res = cur.fetchall()
    if "N" in res[0][1]:
        print("You can't go through a wall, dummy")
    else:
        sql = "Select terrain_type.Id,terrain_square.restriction FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y-1"
        cur.execute(sql)
        res = cur.fetchall()
        if len(res) > 0:
            if res[0][0] == 5:
                print("The forest is too thick, you cannot pass!")
            elif "S" in res[0][1]:
                print("You can't go through a wall, dummy")
            else:
                add_time(square_side, res[0][0])
                sql = "UPDATE player SET player.y = player.y -1"
                cur.execute(sql)
                sql = "select terrain_type.name from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res = cur.fetchall()
                currentSquare = res[0][0]
                print("You entered a " + currentSquare)
        else:
            print("The ocean is that way,it would be suicide!")
            
def move_east():
    sql = "Select terrain_type.Id,terrain_square.restriction FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res = cur.fetchall()
    if "W" in res[0][1]:
        print("You can't go through a wall, dummy")
    else:
        sql = "Select terrain_type.Id,terrain_square.restriction FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x+1"
        cur.execute(sql)
        res = cur.fetchall()
        if len(res) > 0:
            if res[0][0] == 5:
                print("The forest is too thick, you cannot pass!")
            if "E" in res[0][1]:
                print("You can't go through a wall, dummy")
            else:
                add_time(square_side, res[0][0])
                sql = "UPDATE player SET player.x = player.x -1"
                cur.execute(sql)
                sql = "select terrain_type.name from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res = cur.fetchall()
                currentSquare = res[0][0]
                print("You entered a " + currentSquare)
        else:
            print("The ocean is that way,it would be suicide!")
            
def move_west():
    sql = "Select terrain_type.Id,terrain_square.restriction FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
    cur.execute(sql)
    res = cur.fetchall()
    if "E" in res[0][1]:
        print("You can't go through a wall, dummy")
    else:
        sql = "Select terrain_type.Id,terrain_square.restriction FROM terrain_type,terrain_square,player Where terrain_type.ID=terrain_square.type_id and terrain_square.y=player.y and terrain_square.x=player.x-1"
        cur.execute(sql)
        res = cur.fetchall()
        print(res)
        if len(res) > 0:
            if res[0][0] == 5:
                print("The forest is too thick, you cannot pass!")
            if "W" in res[0][1]:
                print("You can't go through a wall, dummy")
            else:
                add_time(square_side, res[0][0])
                sql = "UPDATE player SET player.x = player.x -1"
                cur.execute(sql)
                sql = "select terrain_type.name from terrain_type, terrain_square, player where terrain_type.ID=terrain_square.type_id and terrain_square.x=player.x and terrain_square.y=player.y"
                cur.execute(sql)
                res = cur.fetchall()
                currentSquare = res[0][0]
                print("You entered a " + currentSquare)        
        else:
            print("The ocean is that way,it would be suicide!")
def examine_area():
    sql=("SELECT item_type.name FROM item,item_type,player,terrain_square WHERE item.type_id=item_type.id and player.x=terrain_square.x and player.y=terrain_square.y and item.x=terrain_square.x and item.y=terrain_square.y")
    cur.execute(sql)
    result=cur.fetchall()
    for i in result:
        print(i) 
    for i in range(len(result)):
        print(result[i][0])      
def parse(playerInput):
    playerCaps = playerInput.upper()
    filter = [".", ",", ":", " an ", " a ", "move ", "go ", " in ", " out ", " the ", " and "]
    filteredText = ''.join([c for c in playerCaps if c not in filter])
    playerText = split_line(filteredText)
    
    print(playerText)
    print(filteredText)
    print(())
    if len(playerText) < 1:
        print("Are you an empty vessel?")
    elif playerText[0] == "N" or playerText[0] == "NORTH":
        move_north()
    elif (playerText[0]) == "S" or playerText[0] == "SOUTH":
        move_south()
    elif (playerText[0]) == "W" or playerText[0] == "WEST":
        move_west()
    elif (playerText[0]) == "E" or playerText[0] == "EAST":
        move_east()
    elif (playerText[0]) == "LOOK" or playerText[0] == "L" or playerText[0] == "WATCH" or playerText[0] == "SEE":
        look()
    elif (playerText[0]) == "I":
        inventory()
    elif (playerText[0]) == "DROP":
        drop_item(playerText[1])
    elif (playerText[0]) == "TIME":
        show_time()
    elif (playerText[0])== "EXAMINE":
        if(playerText[1])== "AREA":
            examine_area()
    elif (playerText[0]) == "TAKE" or "PICK" or "PICKUP" or "GRAB":
        if(playerText[1]) == "UP" and playerText[0] == "PICK":
            item = playerText[2]
            for i in range(4):
                if check_item_type(item) == True:  
                    pick_up(item)
                    break
                else:
                    if i == 0:
                        item = (playerText[2] + " " + playerText[3])
                        print(item)
                    elif i == 1:
                        item = (playerText[2] + " " + playerText[3] + " " + playerText[4])
                        print(item)
                    elif i == 2:
                        item(playerText[2] + " " + playerText[3] + " " + playerText[4] + " " + playerText[5])
                        print(item)
                    elif i==3:
                        item(playerText[2] + " " + playerText[3] + " " + playerText[4] + " " + playerText[5]+" "+ playerText[6])
        else:
            item=playerText[1]
            for i in range(3):
                if check_item_type(item) == True:
                    pick_up(item)
                    break
                else:
                    if i == 0:
                        item = (playerText[1] + " " + playerText[2])
                    elif i == 1:
                        item = (playerText[1] + " " + playerText[2] + " " + playerText[3])
                    elif i == 2:
                        item(playerText[1] + " " + playerText[2] + " " + playerText[3] + " " + playerText[4])
                    elif i == 3:
                        item(playerText[1] + " " + playerText[2] + " " + playerText[3] + " " + playerText[4]+" "+ playerText[5])
            
    
    # elif (playerText[0])== "KILL" or "ATTACK" or "ENGAGE" or "FIGHT" or "BATTLE":
        # actions
    # elif (playerText[0])== "I" or "INVENTORY" or "BAG" or "ITEMS":
        # display inventory
    # elif (playerText[0])== "STATS" or "PLAYER" or "CHARACTER" or "CHAR":
        # display player info
    # elif (playerText[0])== "EXAMINE" or "INSPECT" or "STUDY" or "ANALYZE":
        # display info of enemy in the map
    # elif (playerText[0])== "READ":
        # display text
    # elif (playerText[0])== "S" or "SOUTH":
        # actions
    # elif (playerText[0])== "S" or "SOUTH":
        # actions

def main():
    while True:
        
        # out_of_breath()
        # print(player_carry())
        playerInput = input()
        parse(playerInput)
    
main()

#SELECT item_type.name FROM item_type WHERE item_type.name LIKE 'letter from a friend%'