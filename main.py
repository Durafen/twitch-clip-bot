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

CHAT_NAMES_TO_ID = {}

#	Getting channels id from channels names
for channel_name in config.CHANNEL_NAMES:
	channel_id = twitch.get_channel_id(channel_name)

	channel_name = "#" + channel_name
	CHAT_NAMES_TO_ID[channel_name] = str(channel_id)
	print (channel_name + " : " + channel_id)

#	Connecting to Twitch IRC
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	
	s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
	s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 1)
	s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
	s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 5)



	s.connect((config.TWITCH_HOST, config.TWITCH_PORT))
	s.send("PASS {}\r\n".format(config.TWITCH_PASS).encode("utf-8"))
	s.send("NICK {}\r\n".format(config.TWITCH_NICK).encode("utf-8"))

	for channel_name in config.CHANNEL_NAMES:
		s.send("JOIN {}\r\n".format("#" + channel_name).encode("utf-8"))

	connected = True #Socket succefully connected
except Exception as e:
	print(str(e))
	connected = False #Socket failed to connect


#	BOT LOOP
#	--------

def bot_loop():
	
	time.sleep(1)
	print ("Starting Bot Loop")

	while connected:
	
		try:
	
			response = s.recv(1024).decode("utf-8")
			
		except Exception as e:
			print(str(e))
			utility.restart()
			
#		PING-PONG			
		if response == "PING :tmi.twitch.tv\r\n":
	
			try:	
				s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))			
			except IOError as e:
				print ("PONG error:" + str(e))
				utility.restart()

#			print("Pong")

		else:
		
#			Here we go		
			username = re.search(r"\w+", response).group(0) 
			message = CHAT_MSG.sub("", response).rstrip()

			channel = ""			
			try:	
				channel = re.search(r"#\w+", response).group(0) 
			except Exception as e:
				print(str(e))

			print (channel + " | " + username + " : " + message)						

#			clip | !clip
			if message == "!clip" or message == "clip":
            
				channel_id = CHAT_NAMES_TO_ID[channel]
				print (channel_id)

				clip_id = twitch.create_clip(channel_id)
				time.sleep(5)
				
				if clip_id and twitch.is_there_clip(clip_id):
				
					myThread = threading.Timer(5, proccess_clip, args=[clip_id, username,channel])
					myThread.start()
					
					
				else:
					print ("Second try")
					clip_id = twitch.create_clip(channel_id)
					
					if (clip_id):
				
						myThread = threading.Timer(10, proccess_clip, args=[clip_id, username,channel])
						myThread.start()                        
					else:
						utility.chat(s, channel, "Sorry " + username + ", couldn't make your clip")
                    
#			!Hey
			if message == "!hey":
				utility.chat(s, channel, "Hey " + username + "! Whats up?")
#				print (CHAT_NAMES_TO_ID[channel])

#			!help
			if message == "!help":
				utility.chat(s, channel,  username + ", I'm the clipping bot. type \"clip\" or \"!clip\" in chat, I'll clip the last 25 sec and post the link.")
					
            
		for pattern in COMMANDS:
			if re.match(pattern[0], message):
				utility.chat(s, channel,  pattern[1])

		time.sleep(0.1)
		    
			
#			print(username + ": " + response)
#			for pattern in config.BAN_PAT:
#				if re.match(pattern, message):
#					utility.ban(s, username)
#					break

#	Thread for proccessing clip after X time
def proccess_clip(clip_id,username,channel_name):
	
#	print (clip_id)    

	if twitch.is_there_clip(clip_id):
		clip_url = "https://clips.twitch.tv/" + clip_id 
#		print (clip_url)
		utility.chat(s, channel_name, clip_url)
		utility.write_tofile(clip_url + "\n")

	else:
		utility.chat(s, channel_name, "Sorry " + username + ", twitch couldn't make the clip")
			

#  __MAIN __
#  ---------

if __name__ == "__main__":
	

#	channel_id = twitch.get_channel_id("AdmiralBahroo")
#	print (channel_id)

	bot_loop()

	
#	access_token = twitch.get_access_token()
#	twitch.auth1()
#	print (access_token)
	
	
	
