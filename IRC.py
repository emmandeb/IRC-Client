from Tkinter import *
import socket, string # IRC
import threading
import os

import time

#########################
# IRC Stuff
server = 'irc.freenode.net'
port = 6667
nickname = 'test_client'
channel = '#freenode'  


#open a socket to handle the connection
IRC = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#open a connection with the server
def irc_conn():
    IRC.connect((server, port))

#simple function to send data through the socket
def send_data(command):
    IRC.send(command + '\n')

#join the channel
def join(channel):
    send_data("JOIN %s" % channel)

#send login data (customizable)
def login(nickname, username='user', password = None, realname='Pythonist', hostname='Helena', servername='Server'):
    send_data("USER %s %s %s %s" % (username, hostname, servername, realname))
    send_data("NICK " + nickname)
#########################

class GET_USERS():
    def __init__(this):
        send_data("names "+channel+"\r\n")

def update_user_list(data):
    listbox.delete(0, END)
    e.delete(0, END)
    for user in data:
        listbox.insert(END, user)
    
    
#########################

def update(null):
    message = e.get()
    message_listbox.insert(END, message)        # Append text then
    message_listbox.yview(END)                  # auto scroll to it

def send(message):
    message = e.get()
    if ( message.startswith('!quit') ):         # turn into a function, call at intervals
        #send_data("/quit "+message+"\r\n") # add room for part message
        send_data("/quit \r\n")
        quit()

    elif ( message.startswith('/') ):  ## DOESNT WORK! 
        #send_data(message+"\r\n")
        send_data(message.strip( '/' )+"\r\n")
        message_listbox.insert(END, "PRIVATE MESSAGE TO=> "+nickname+": "+e.get())
        message_listbox.yview(END)                  # auto scroll
        e.delete(0, END)

    elif ( message.startswith('!users') ):
           send_data("names "+channel+"\r\n")
          
 ########################
# Move das bot
    elif ( message.startswith('!left') ):
           send_data("PRIVMSG "+channel+" :m4(f, 0.25)\r\n")
    elif ( message.startswith('!right') ):
           send_data("PRIVMSG "+channel+" :m4(b, 0.25)\r\n")
    elif ( message.startswith('!up') ):
           send_data("PRIVMSG "+channel+" :m3(f, 0.25),wait,m2(f, 0.25)\r\n")
    elif ( message.startswith('!down') ):
           send_data("PRIVMSG "+channel+" :m3(b, 0.25),wait,m2(b, 0.25)\r\n")

    else:
        message_listbox.insert(END, nickname+": "+e.get())
        message_listbox.yview(END)                  # auto scroll
        send_data("PRIVMSG "+channel+" :"+str(e.get())+"\r\n") #needs some checking gawd
        e.delete(0, END)

# Work around for right now
# this and the update() function should be one with one another
def update_incoming(message):
    message_listbox.insert(END, message)
    message_listbox.yview(END)                  # auto scroll to it



# temp end function
#stay_connected = 1
def quit():
    #sys.exit()
    #stay_connected = 0
    master.destroy()
    os._exit(1) # maybe sys.exit() later?
    
########################
class GUI():
    def __init__(this):
        global message_listbox  #chatbox
        global listbox      #user lists, rename later
        global e        #entry box
        global master       # temp work around, should be removed
        master = Tk()
        master.wm_title('Quick')                # set the window title

        # Menu bar(TO DO)
        # http://www.pythonware.com/library/tkinter/introduction/x5819-patterns.htm
        #########################
        # Main Window
        # encompasses the User List and Message Box
        main_window = Frame(master)
        #########################
        


        #########################
        # Message Box
        # This is where all messages are shown
        message_box = Frame(main_window)
        scrollbar = Scrollbar(message_box)      # Message Scroll bar
        message_listbox = Listbox(message_box, width=45, height=20, yscrollcommand=scrollbar.set)
        scrollbar.config(command=message_listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        message_box.pack(side=LEFT)
        message_listbox.pack()
        #########################

        #########################
        # User List
        user_list = Frame(main_window)
        scrollbar = Scrollbar(user_list)       # Message Scroll bar
        listbox = Listbox(user_list, width=15, height=20, yscrollcommand=scrollbar.set)
        scrollbar.config(command=listbox.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        user_list.pack(side=RIGHT)
        listbox.pack()
        #########################

        #########################
        # This is where you enter commands and text
        e = Entry(master, width=60)
        e.pack(side=BOTTOM)
        e.focus_set()
        e.txt = StringVar()
        e.bind("<Return>", send)
        #########################    
        
        main_window.pack()
        mainloop()

#########################
class TEMP_IRC_CLASS_SORRY_CHANGE_LATER():
    def __init__(this):
        global buffer
        global msg
        
        #########################
        # Connect to IRC
        # Helpful list of commands
        # http://www.irchelp.org/irchelp/ircprimer.html#Commands
        irc_conn()
        login(nickname)
        join(channel)


        #while (stay_connected == 1):
        while True:
            buffer = IRC.recv(1024)
            msg = string.split(buffer)
            #print "test1"

            ##########
            nick_before = msg[0][:string.find(msg[0],"!")]
            nick_name = string.lstrip(nick_before, ':')
            message_before = ' '.join(msg[3:])
            message = string.lstrip(message_before, ':')
            print nick_name+message
            ##########

            # msg[2] == channel, but we need to do a str.lowercase
            
            if msg[0] == "PING": #check if server has sent ping command
                send_data("PONG %s" % msg[1]) #answer with pong as per RFC 1459

            # Print Chat
            if msg [1] == 'PRIVMSG' and msg[2] == channel:
                data = nick_name+": "+message
                update_incoming(data)
                
                
                
            
            # Private messages
            if msg [1] == 'PRIVMSG' and msg[2] == nickname:
                data = "PRIVATE MESSAGE FROM => "+nick_name+": "+message
                update_incoming(data)
            
            #private message with command
            #if msg [1] == 'PRIVMSG' and msg[2] == NICKNAME and message == "!on":
            #but why?
                
            

            # Send Version Data on Request so we don't look like a bot
            if msg [1] == 'PRIVMSG' and msg[2] == channel  and message == "VERSION":
                version_string = "VERSION QuickIRC alpha"
                send_data("PRIVMSG "+nick_name+" :"+version_string+"\r\n")
            #print "test2"

            #print "test3"

            #update_users_box("test")
            if ( nick_name.find(".freenode.net") and message.startswith("@ "+channel) and message.endswith("list.") == False ):
                users = message.split(" ")
                update_user_list(users[2:])
                
            if (message == ""):
                update_incoming(nick_name+" Joined "+channel)
                GET_USERS()

            # parting users
            #if (message == '"LEAVING"'):
            #    GET_USERS()
            
#########################


class newThread ( threading.Thread ):
    def run ( self ):
        GUI()

class new_irc_connection ( threading.Thread ):
    def run ( self ):
        TEMP_IRC_CLASS_SORRY_CHANGE_LATER()



new_irc_connection().start()        # SRSLY Need to work on exiting
newThread().start()                 # the threads cleanly!
