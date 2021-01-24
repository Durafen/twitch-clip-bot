#!/usr/bin/env python3

import socket
import ssl
import time
import re
import threading

import twitch
import config
import utility
import debug

COMMANDS = [
    #	[r"!discord", "the official discord: ____"]
]

CHAT_MSG = re.compile(r":\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")

CHAT_NAMES_TO_ID = {}

#	Getting channels id from channels names
for channel_name in config.CHANNEL_NAMES:
    channel_id = twitch.get_channel_id(channel_name)

    channel_name = "#" + channel_name
    CHAT_NAMES_TO_ID[channel_name] = str(channel_id)
    utility.print_toscreen(channel_name + " : " + channel_id)

#	Connecting to Twitch IRC
try:
    s_p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s = ssl.wrap_socket(s_p)

    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 1)
    s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
    s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 5)

    s.connect((config.TWITCH_HOST, config.TWITCH_PORT))
    s.send("PASS {}\r\n".format(config.TWITCH_PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.TWITCH_NICK).encode("utf-8"))

    for channel_name in config.CHANNEL_NAMES:
        s.send("JOIN {}\r\n".format("#" + channel_name).encode("utf-8"))

    connected = True  # Socket succefully connected
except Exception as e:
    debug.output_error(debug.lineno() + " - " + str(e))
    connected = False  # Socket failed to connect


#	BOT LOOP
#	--------

def bot_loop():
    time.sleep(0.5)
    utility.print_toscreen("Starting Bot Loop")

    while connected:

        response = ""

        try:

            response = s.recv(1024).decode("utf-8")

        except Exception as e:
            debug.output_error(debug.lineno() + " - " + str(e))
            utility.restart()

        #		PING-PONG
        if re.search("PING :tmi.twitch.tv",response):

            try:
                s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
# 		 utility.print_toscreen("Pong")
#                debug.output_debug ("PONG")
            except IOError as e:
                debug.output_error(debug.lineno() + " - " + "PONG error " + str(e))
                utility.restart()

        find_all = re.findall(CHAT_MSG, response)

        for found in find_all:

            username = ""
            channel = ""
            message = ""

            try:

                username = re.search(r"\w+", found).group(0)
                channel = re.search(r"#\w+", found).group(0)
                message = response[response.find(found) + len(found):]

                start = re.search(CHAT_MSG, message)
                if start:
                    message = message[0:start.start()]
                else:
                    message = message

                utility.print_usertoscreen(channel, username, message.rstrip())
                message = message.lower().rstrip()

            except Exception as e:
                debug.output_error(debug.lineno() + " - " + str(e))

            #			clip | !clip
            if message == "!clip" or message == "clip" or message == "clip it":

                channel_id = CHAT_NAMES_TO_ID[channel]
                debug.output_debug(channel + " | " + username + ": " + message)

                clip_thread = threading.Timer(5, create_clip, args=[channel, channel_id, username])
                clip_thread.start()

            #           			!Hey
#            if message == "!hey" or message == "hi" or message == "hey" or message == "hello" or message == "heyguys":
#               utility.chat(s, channel, "Hey " + username + ", Welcome to the stream!")
#				utility.print_toscreen(CHAT_NAMES_TO_ID[channel])

            #			!help
            if message == "!help":
                utility.chat(s, channel,
                             "Hi, I'm the clipping bot. type \"clip\" or \"!clip\" in chat, I'll clip the last 25 sec and post the link.")

            if re.search(config.TWITCH_NICK, message):
                debug.output_debug(channel + " | " + username + ": " + message)


#        for pattern in COMMANDS:
#            if re.match(pattern[0], message):
#                utility.chat(s, channel, pattern[1])


#	Thread for creating clip
def create_clip(channel, channel_id, username):
       
#   if twitch.is_stream_live(channel_id):
    if True:
        clip_id = twitch.create_clip(channel_id)
        time.sleep(5)
    
        if clip_id and twitch.is_there_clip(clip_id):
    
            clip_proccess_thread = threading.Timer(0, proccess_clip, args=[clip_id, username, channel])
            clip_proccess_thread.start()
        
        else:
            debug.output_debug("Second try")
            clip_id = twitch.create_clip(channel_id)
            time.sleep(10)

            if (clip_id):
    
                clip_proccess_thread = threading.Timer(0, proccess_clip, args=[clip_id, username, channel])
                clip_proccess_thread.start()
            else:
                utility.chat(s, channel, "Sorry " + username + ", couldn't make your clip")
    else:
        utility.chat(s, channel, username + ", the stream is offline, clipping is disabled.")


#	Thread for proccessing clip after X time
def proccess_clip(clip_id, username, channel_name):

    if twitch.is_there_clip(clip_id):
        clip_url = "https://clips.twitch.tv/" + clip_id

        utility.chat(s, channel_name, clip_url)
        utility.write_tofile(clip_url + "\n")

    else:
        utility.chat(s, channel_name, "Sorry " + username + ", Twitch couldn't make the clip.")


#  ---------
#    MAIN  
#  ---------

if __name__ == "__main__":
    bot_loop()

