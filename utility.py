#!/usr/bin/env python

import datetime
import os
import random
import sys
import time

from sty import fg

import debug
import config

ROWS, COLUMNS = os.popen('stty size', 'r').read().split()
MAX_MSG_SIZE: int = int(COLUMNS) - 44

EXCLUDE_COLORS = ["0", "7", "15", "16", "17"]
USER_COLORS = {}


def chat(sock, channel_name, msg):
    (sock.send(("PRIVMSG {} :{}\r\n".format(channel_name, msg)).encode("UTF-8")))

    print_usertoscreen(channel_name, config.TWITCH_NICK , "--> " + msg)
    debug.output_debug(channel_name + " |-> " + msg)


def restart():
    print_usertoscreen("system", "bot" , "Restarting")
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

    lines = 0
    while len(message) > 0:
        if len(message) < MAX_MSG_SIZE:
            msg = message
            message = ""
        else:
            msg = message[:MAX_MSG_SIZE]
            message = message[MAX_MSG_SIZE:len(message)]

        lines += 1
        if lines == 1:
            print('{:<7s}{:<16s}{:s}{:s}{:<15s}{:s}{:^3s}{:s}'.format(currentDT.strftime("%H:%M"), channel, "| ",
                                                                      fg(int(color)), username, fg.rs, ":", msg))
        else:
            print(
                '{:<7s}{:<16s}{:s}{:s}{:<15s}{:s}{:^3s}{:s}'.format("", "", "| ", fg(int(color)), "", fg.rs, ":", msg))


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
