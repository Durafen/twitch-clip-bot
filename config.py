#!/usr/bin/env python

TWITCH_HOST = "irc.chat.twitch.tv"         # This is Twitchs IRC server
TWITCH_PORT = 6697                         # Twitchs IRC server listens on port 6767
TWITCH_NICK = "BOT TWITCH NICK"            # Twitch username your using for your bot
TWITCH_PASS = "OATH TWITCH TOKEN"          # Twitch OAuth token from https://twitchapps.com/tmi/

DEBUG = 1
TWITCH_RATE = (20/30) # messages per seccond
CHANNEL_NAMES = ["channel1","channel2","channel3"]

CLIENT_ID = "TWITCH APP CLIENT ID"         # https://dev.twitch.tv/console/apps/
CLIENT_SECRET = "TWITCH APP CLIENT SECRET" # https://dev.twitch.tv/console/apps/
CLIENT_REFRESH_TOKEN = "TWITCH APP REFRESH TOKEN" # See instuction bellow

#RUN IN BROWSER (change CLIENT_ID and CLIENT SECRET)
#https://id.twitch.tv/oauth2/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=http://localhost&scope=clips:edit
#Take the code from url response and get the refresh token from terminal (change CLIENT_ID, CLIENT_SECRET, CODE)
#curl -X POST -k -i 'https://id.twitch.tv/oauth2/token?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&code=CODE&grant_type=authorization_code&redirect_uri=http://localhost'
