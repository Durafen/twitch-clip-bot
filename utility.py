#!/usr/bin/env python

import config
import socket
import time
import datetime
import sys
import os
import random
import debug
from sty import fg, bg, ef, rs

ROWS, COLUMNS = os.popen('stty size', 'r').read().split()
MAX_MSG_SIZE = int(COLUMNS) - 46

EXCLUDE_COLORS = ["0", "7", "15", "16", "17"]
USER_COLORS = {}


def chat(sock, channel_name, msg):
    (sock.send(("PRIVMSG {} :{}\r\n".format(channel_name, msg)).encode("UTF-8")))

    print_toscreen(channel_name + " |-> " + msg)
    debug.output_debug(channel_name + " |-> " + msg)


def restart():
    print_toscreen("Restarting", "9")
    time.sleep(5)
    # os.execv(__file__, sys.argv)
    os.execv(sys.executable, ['python3'] + sys.argv)


def write_tofile(text):
    file = open("cliplog.txt", "a")
    file.write(text)
    file.close()


def print_toscreen(text, username="", color="15"):
    currentDT = datetime.datetime.now()

    print(currentDT.strftime("%H:%M") + "  " + text)


def print_usertoscreen(channel, username, message):
    currentDT = datetime.datetime.now()

    color = "15"
    if not (username == ""):
        color = get_user_color(username)

    username = (username[:15] + '') if len(username) > 15 else username
    channel = (channel[:15] + '') if len(channel) > 15 else channel
    
    msg = (message[:MAX_MSG_SIZE] + '..') if len(message) > MAX_MSG_SIZE else message

    print('{:<7s}{:<16s}{:s}{:s}{:<15s}{:s}{:^3s}{:s}'.format(currentDT.strftime("%H:%M"), channel, "| ", fg(int(color)), username, fg.rs, ":", msg))


def get_user_color(username):
    color = "15"

    if username in USER_COLORS:
        color = USER_COLORS[username]
    else:
        color = "0"
        while color in EXCLUDE_COLORS:
            color = str(random.randint(0, 220))

#        print_toscreen(username + " color " + color)
        USER_COLORS[username] = color
#        EXCLUDE_COLORS.append(color)

    return color
