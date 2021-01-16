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
    utility.print_toscreen(channel_name + " : " + channel_id)

#	Connecting to Twitch IRC
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
    s.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 5)

    s.connect((config.TWITCH_HOST, config.TWITCH_PORT))
    s.send("PASS {}\r\n".format(config.TWITCH_PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(config.TWITCH_NICK).encode("utf-8"))

    for channel_name in config.CHANNEL_NAMES:
        s.send("JOIN {}\r\n".format("#" + channel_name).encode("utf-8"))

    connected = True  # Socket succefully connected
except Exception as e:
    utility.print_toscreen(str(e))
    connected = False  # Socket failed to connect


#	BOT LOOP
#	--------

def bot_loop():
    time.sleep(0.5)
    utility.print_toscreen("Starting Bot Loop")

    while connected:

        try:

            response = s.recv(1024).decode("utf-8")

        except Exception as e:
            utility.print_toscreen(str(e))
            utility.restart()

        #		PING-PONG
        if response == "PING :tmi.twitch.tv\r\n":

            try:
                s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            except IOError as e:
        #        utility.print_toscreen("PONG error:" + str(e))
                utility.restart()

        #			utility.print_toscreen("Pong")

        else:

            #			Here we go
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response).rstrip()
            message = message.lower()

            channel = ""
            try:
                channel = re.search(r"#\w+", response).group(0)
            except Exception as e:
                utility.print_toscreen(str(e))

            utility.print_usertoscreen(channel, username, message)

            #			clip | !clip
            if message == "!clip" or message == "clip":

                channel_id = CHAT_NAMES_TO_ID[channel]

#                if twitch.is_stream_live(channel_id):
                if True:
                    clip_id = twitch.create_clip(channel_id)
                    time.sleep(5)

                    if clip_id and twitch.is_there_clip(clip_id):

                        myThread = threading.Timer(5, proccess_clip, args=[clip_id, username, channel])
                        myThread.start()


                    else:
                        utility.print_toscreen("Second try", "9")
                        clip_id = twitch.create_clip(channel_id)

                        if (clip_id):

                            myThread = threading.Timer(10, proccess_clip, args=[clip_id, username, channel])
                            myThread.start()
                        else:
                            utility.chat(s, channel, "Sorry " + username + ", couldn't make your clip")
                else:
                    utility.chat(s, channel, username + ", the stream is offline, clipping is disabled.")

#           			!Hey
#            if message == "!hey" or message == "hi" or message == "hey" or message == "hello" or message == "heyguys":
#               utility.chat(s, channel, "Hey " + username + ", Welcome to the stream!")
#				utility.print_toscreen(CHAT_NAMES_TO_ID[channel])

            #			!help
            if message == "!help":
                utility.chat(s, channel,
                             "Hi, I'm the clipping bot. type \"clip\" or \"!clip\" in chat, I'll clip the last 25 sec and post the link.")

        for pattern in COMMANDS:
            if re.match(pattern[0], message):
                utility.chat(s, channel, pattern[1])

        time.sleep(0.1)


#	Thread for proccessing clip after X time
def proccess_clip(clip_id, username, channel_name):
    #	utility.print_toscreen(clip_id)

    if twitch.is_there_clip(clip_id):
        clip_url = "https://clips.twitch.tv/" + clip_id
        #		utility.print_toscreen(clip_url)
        utility.chat(s, channel_name, clip_url)
        utility.write_tofile(clip_url + "\n")

    else:
        utility.chat(s, channel_name, "Sorry " + username + ", Twitch couldn't make the clip.")


#  __MAIN __
#  ---------

if __name__ == "__main__":
    bot_loop()

