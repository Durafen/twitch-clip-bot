#!/usr/bin/env python

import socket
import time
import re
import threading

import twitch
import config
import utility


COMMANDS = [
#	[r"!discord", "the official discord: ____"]
]

CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

try:
	s = socket.socket()
	
	s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
	s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 1)
	s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
	s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 5)

	s.connect((config.HOST, config.PORT))
	s.send("PASS {}\r\n".format(config.PASS).encode("utf-8"))
	s.send("NICK {}\r\n".format(config.NICK).encode("utf-8"))
	s.send("JOIN {}\r\n".format(config.CHAN).encode("utf-8"))
	connected = True #Socket succefully connected
except Exception as e:
	print(str(e))
	connected = False #Socket failed to connect

def bot_loop():
	
	while connected:
	
		try:
	
			response = s.recv(1024).decode("utf-8")
			
		except Exception as e:
			print(str(e))
			utility.restart()
			
		if response == "PING :tmi.twitch.tv\r\n":
	
			try:	
				s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))			
			except IOError as e:
				print "PONG error:", str(e)
				utility.restart()

#			print("Pong")

		else:
		
			username = re.search(r"\w+", response).group(0) 
			message = CHAT_MSG.sub("", response)
						
			print (username + " : " + message.rstrip())						

			if message.rstrip() == "!clip" or message.rstrip() == "clip":
            
				clip_id = twitch.create_clip(config.CHANNEL_ID)
				time.sleep(5)
				
				if clip_id and twitch.is_there_clip(clip_id):
				
					myThread = threading.Timer(5, proccess_clip, args=[clip_id, username])
					myThread.start()
					
					
				else:
					print "Second try"
					clip_id = twitch.create_clip(config.CHANNEL_ID)
					
					if (clip_id):
				
						myThread = threading.Timer(10, proccess_clip, args=[clip_id, username])
						myThread.start()
                                            
					else:
						utility.chat(s,"Sorry " + username + ", couldn't make your clip")
                    

			if message.rstrip() == "!hey":
				utility.chat(s,"Hey " + username + "! Whats up?")

			if message.rstrip() == "!help":
				utility.chat(s, username + ", I'm the clipping bot. type \"clip\" or \"!clip\" in chat, I'll clip the last 25 sec and post the link.")
					
            
		for pattern in COMMANDS:
			if re.match(pattern[0], message):
				utility.chat(s, pattern[1])

		time.sleep(0.1)
		    
			
#			print(username + ": " + response)
#			for pattern in config.BAN_PAT:
#				if re.match(pattern, message):
#					utility.ban(s, username)
#					break

def proccess_clip(clip_id,username):
	print clip_id
    
	if twitch.is_there_clip(clip_id):
		clip_url = "https://clips.twitch.tv/" + clip_id 
#		print clip_url
		utility.chat(s,clip_url)
		write_tofile(clip_url + "\n")

	else:
		utility.chat(s,"Sorry " + username + ", twitch couldn't make the clip")
			

if __name__ == "__main__":
	
 
	bot_loop()

	
#	access_token = twitch.get_access_token()
#	twitch.auth1()
#	print access_token	
	
	
	