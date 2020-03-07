#!/usr/bin/env python



HOST = "irc.twitch.tv"              # This is Twitchs IRC server
PORT = 6667                         # Twitchs IRC server listens on port 6767
NICK = "BOT TWITCH NICK"            # Twitch username your using for your bot
PASS = "OATH TWITCH TOKEN" # your Twitch OAuth token
CHAN = "CHANNEL WITH # prefix"                   # the channel you want the bot to join.

RATE = (20/30) # messages per seccond
BAN_PAT = [
    r"swear",
    r"some_pattern"
]


CHANNEL_ID = "CHANNEL ID TO CLIP"

CLIENT_ID = "TWITCH APP CLIENT ID"
CLIENT_SECRET = "TWITCH APP CLIENT SECRET"
CLIENT_REFRESH_TOKEN = "TWITCH APP REFRESH TOKEN"


