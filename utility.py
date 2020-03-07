import config
import socket
import time
import sys
import os


def chat(sock, msg):
	"""
	Send a chat message to the server.
	Keyword arguments:
	sock -- the socket over which to send the message
	msg  -- the message to be sent
	"""
	sock.send(("PRIVMSG {} :{}\r\n".format(config.CHAN, msg)).encode("UTF-8"))
	print "Sending -> " + msg
#	print msg

def ban(sock, user):
	"""
	Ban a user from the current channel.
	Keyword arguments:
	sock -- the socket over which to send the ban command
	user -- the user to be banned
	"""
	chat(sock, ".ban {}".format(user))

def timeout(sock, user, secs=600):
	"""
	Time out a user for a set period of time.
	Keyword arguments:
	sock -- the socket over which to send the timeout command
	user -- the user to be timed out
	secs -- the length of the timeout in seconds (default 600)
	"""
	chat(sock, ".timeout {}".format(user, secs))
	
	

def restart():
	print "Restarting"
	time.sleep (5)
	#os.execv(__file__, sys.argv)	
	os.execv(sys.executable, ['python'] + sys.argv)
	
