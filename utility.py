#!/usr/bin/env python

import config
import socket
import time
import datetime
import sys
import os
import random
from sty import fg, bg, ef, rs

USER_COLORS = {}

def chat(sock, channel_name, msg):

	(sock.send(("PRIVMSG {} :{}\r\n".format(channel_name, msg)).encode("UTF-8")))

	print_toscreen(channel_name + " |-> " + msg)

#def ban(sock, user):

#	chat(sock, ".ban {}".format(user))

#def timeout(sock, user, secs=600):

#	chat(sock, ".timeout {}".format(user, secs))
	
	
def restart():
	print_toscreen("Restarting","9")
	time.sleep (5)
	#os.execv(__file__, sys.argv)	
	os.execv(sys.executable, ['python3'] + sys.argv)
	

def write_tofile(text):
	file = open("cliplog.txt","a") 	
	file.write(text)
	file.close() 

def print_toscreen(text, username = "",  color = "15"):
	currentDT = datetime.datetime.now()

	print( currentDT.strftime("%H:%M") + "\t" + text )

def print_usertoscreen(channel, username, message):
	currentDT = datetime.datetime.now()

	color = "15"
	if not(username == ""):
		color = get_user_color(username)	

#	print(fg(int(color)) + currentDT.strftime("%H:%M") + fg.rs + " " + text )
	print(currentDT.strftime("%H:%M") + "\t" + channel + " | " + fg(int(color)) + username + fg.rs + "\t: " + message)						



def get_user_color(username):
	color = "15"

	if username in USER_COLORS:
		color = USER_COLORS[username]
	else:
		color = 0
		while color in {0,16,17}:
			color = str(random.randint(0, 87))
			print_toscreen(username + " color " + color)

		USER_COLORS[username] = color

	return color


