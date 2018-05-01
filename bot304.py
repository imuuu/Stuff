import sys
import time
import random
import datetime
import telepot
import subprocess
import shlex
from nsp import Nsp
import joke
import quiz
from random import shuffle
import flagDayyy

import callWeather

#when running pass in the token as the first parameter e.g. python3.4 file.py token
TOKEN = sys.argv[1] 

quiz_bool = False
quiz_guesses = 1

def handle(msg):
    print("\n")
    
    username = msg['from']['username']
    permissions = read_file('permissions', '~/Desktop/').split('\n')
    
    if  str(username) in permissions:
        permission = True
    else:
        permission = False
        
    print('User: '+username)   
    print('Permission: '+str(permission))
    
    chat_id = msg['chat']['id']
    command = msg['text']
    
    if command[0] is not '/':
        quiz_game(chat_id, command)
        return
    
    tag = command.split()[0]
    args = arguments(command)
    
    print ('Command: %s' % tag)
    print ("Args: %s" % args)
    
    if tag in ["/bash","/b"]:
        if permission:
            bot.sendMessage(chat_id, bash(args))
        else:
            bot.sendMessage(chat_id, 'You do not have permission.')
            
    elif tag in ["/math","/m"]:
        bot.sendMessage(chat_id, math(args))
        
    elif tag == "/hello":
        bot.sendMessage(chat_id, 'Hello World from githubbbb')
    elif tag == '/fd':
        if args=='':
            today=datetime.datetime.now()
            todaydate=today.strftime('%d.%m')
            flagday=flagDayyy.flagDay(todaydate)
            
            if flagday[0]==None:
                fdString=flagday[1]
            elif flagday[1]==None:
                fdString="Today there is no flag day xD"
            else:
                fdString=flagday[0]+'\n\n'+flagday[1]
            
        else:
            flagday=flagDayyy.flagDay(args)
            if flagday[0]==None:
                fdString=flagday[1]
            elif flagday[1]==None:
                fdString="Today there is no flag day xD"
            else:
                fdString=flagday[0]+'\n\n'+flagday[1] 
        if not fdString:
            fdString = 'That day isnt flag day'
        bot.sendMessage(chat_id,fdString) 
       
    elif tag == "/hi":
        bot.sendMessage(chat_id, 'Miten menee?')
    elif tag == "weather":
        weather=callWeather.weather()
        days=weather[0]
        dayTimes=weather[1]
        dayTemp=weather[2]
        
        weatherString=''
        if args=='':
            bot.sendMessage(chat_id,weather[3])
            
        else:
            if args =='all':
                for i in range(len(dayTimes)):
                    weatherString+=str(days[i])+' klo '+ str(dayTimes[i]) +' temp'+str(dayTemp[i])+'\n'
                bot.sendMessage(chat_id, weatherString)
            
            
    elif tag == "/time":
        bot.sendMessage(chat_id, bash("date"))
        
    elif tag in ['/joke','/j']:
        joke, answer = bash_joke(args)
        bot.sendMessage(chat_id, joke)
        if answer:
            time.sleep(3)
            bot.sendMessage(chat_id, answer)
            
    elif tag in ["/wiki", "/wikipedia"]:
        bot.sendMessage(chat_id, wiki(args))
        
    elif tag == '/quiz':
        quiz_game(chat_id, command)
    
    elif tag == '/help' and args:
        bot.sendMessage(chat_id, help(args))
    else:
        bot.sendMessage(chat_id, help('help'))
        
def bash(args, output_bool=True):
    output = subprocess.check_output(args, stderr=subprocess.STDOUT, shell=True)
    if output:
        output = str(output, 'utf8')
        if output_bool:
            print("Output: %s" % output.replace('\n','\n\t'))
        return output
    return "Done"    

def bash_joke(args):
    file = read_file('jokes.txt')
    files = file.split('\n')
    temp = args.partition(' . ')
    args = temp[0].upper()+temp[1]+temp[2]
    joke = ''
    if not args:
        shuffle(files)
        joke = files[0]
    else:
        name = args.split(' . ', 1)[0]
        for line in files:
            if line.split(' . ', 1)[0] == name:
                joke = line
                break
        if ' . ' not in args:
            if not joke:
                return 'There is no joke of that name.', ''
        else:
            if joke.split(' . ', 1)[0] == name:
                return 'Name is allready in use.', ''
            print(add_to_file('jokes.txt', [args]))
            return 'done', ''
    joke_list = joke.replace(' . ', '\n', 1).rsplit(' : ', 1)
    joke = joke_list[0]
    if len(joke_list) > 1:
        return joke, joke_list[1]
    return joke, ''

def help(name):
    file = read_file('help')
    files = file.split('\n')
    name = name.upper()
    content = []
    commands = []
    for line in files:
        line_list = line.split(' . ', 1)
        if line_list[0] == name:
            content.append(line_list[1])
        if line_list[0]:    
            commands.append(line_list[0].capitalize())
    if not content:
        return 'There is no command of that name.'
    if name == 'HELP':
        return '\n'.join(content) + '\nCommands: ' + ', '.join(set(commands)) 
    return '\n'.join(content)

def read_file(filename, path='~/vattu/'):
    return bash('cat '+path+filename, False)

def add_to_file(filename, content_list=[], path='~/vattu/', gap='\n'):
    file = read_file(filename, path=path)
    if not file:
        content = gap.join(content_list)
        msg = 'New file created.'
        output = bash('echo -n "'+content+'" > '+path+filename, False)
    else:
        content = gap.join(content_list)
        msg = 'File modified.'
        output = bash('echo -n "'+gap+content+'" >> '+path+filename, False)    
    return output, msg   
    
def wiki(args):
    if args:
        args = args.split()
    else:
        return "Use /wiki ( .en, .fi, .ru etc. ) Your search\ne.g. /wiki .fi one punch man"
    
    i = 0
    
    if args[i][0]=='.':
        language = args[i][1:]
        i += 1
    else:
        language = "en"
        
    search = '_'.join(args[i:])
    
    url = "https://{0:s}.wikipedia.org/w/index.php?search={1:s}".format(language, search)
    print("URL: " + url)
    return url    

def math(args):
    nsp = Nsp()
    args = args.replace(' ','')
    result = nsp.eval(args)
    result = "{0:s} = {1:g}".format(args,result)
    print (result)
    return result
    
def arguments(command):
    args = shlex.split(command)
    args.pop(0) # .pop(0) removes ex. '/bash'
    args = ' '.join(args)
    return args

def quiz_game(chat_id, command):
    global quiz_bool
    if not quiz_bool:
        quiz_bool = True
        print('quiz starts')
        quiz_guesses = 0
        quiz.quiz_start(read_file('quiz_questions'), command.split()[1])
        next = quiz.quiz_next()
        if next:
            bot.sendMessage(chat_id, next)
        else:
            quiz_bool = False
            bot.sendMessage(chat_id, 'Quiz has ended.')
    elif command.split()[1] == '/quiz':
        print('quiz ends')
        bot.sendMessage(chat_id, 'Quiz has ended.')
    else:
        skip = command.lower() in ['skip'] or quiz_guesses >= 3
        if quiz.quiz_check(command) or skip:
            if not skip:
                bot.sendMessage(chat_id, command + ' is correct')
            next = quiz.quiz_next()
            if next:
                quiz_guesses = 1
                bot.sendMessage(chat_id, next)
            else:
                quiz_bool = False
                print('quiz ends')
                bot.sendMessage(chat_id, 'Quiz has ended.')
        else:
            quiz_guesses += 1
            bot.sendMessage(chat_id, command + ' is Incorrect.\nYou have '+str(3-quiz_guesses)+' guesses left.')            

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)

print ('I am listening...')

while 1:
    time.sleep(10)
        
#https://docs.python.org/3/library/subprocess.html
#https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output

#https://stackoverflow.com/questions/2371436/evaluating-a-mathematical-expression-in-a-string
