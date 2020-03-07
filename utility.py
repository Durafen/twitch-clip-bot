#!/usr/bin/env python

import config
import socket
import time
import sys
import os


def chat(sock, channel_name, msg):

	(sock.send(("PRIVMSG {} :{}\r\n".format(channel_name, msg)).encode("UTF-8")))

	print (channel_name + " -> " + msg)
#	print msg

#def ban(sock, user):

#	chat(sock, ".ban {}".format(user))

#def timeout(sock, user, secs=600):

#	chat(sock, ".timeout {}".format(user, secs))
	
	
def restart():
	print ("Restarting")
	time.sleep (5)
	#os.execv(__file__, sys.argv)	
	os.execv(sys.executable, ['python3'] + sys.argv)
	

def write_tofile(text):
	file = open("cliplog.txt","a") 	
	file.write(text)
	file.close() 

