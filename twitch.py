#!/usr/bin/env python

import urllib
import urllib.parse
import urllib.request

from urllib.error import HTTPError, URLError

import json
import threading

import utility
import config


access_token  = ""


def do_refresh_token():
	
    get_access_token() 
    utility.print_toscreen("Token Refreshed")
    utility.print_toscreen(access_token)

    myThread.run()	
	


def auth(code):

    url = "https://id.twitch.tv/oauth2/token"
#    url = "https://id.twitch.tv/oauth2/token?client_id=" + config.CLIENT_ID + "&client_secret="  + config.CLIENT_SECRET + "&code=lv1tcwmo8gidqzkj2ipk62po8evg16&grant_type=authorization_code&redirect_uri=http://localhost"
    data = urllib.parse.urlencode({
                                    'client_id' : config.CLIENT_ID,
                                    'client_secret' : config.CLIENT_SECRET,                                   
                                    'code' : code,
                                    'grant_type' : 'authorization_code',
                                    'redirect_uri' : 'http://localhost'
                                    })
    
    data = data.encode('utf-8')
    req = urllib.request.Request(url)

    response = urllib.request.urlopen(req, data = data)
    data = json.load(response)   
    utility.print_toscreen(data)


def get_access_token():

#    url = "?grant_type=refresh_token&refresh_token=" + config.CLIENT_REFRESH_TOKEN + "&client_id=" + config.CLIENT_ID + "&client_secret=" + config.CLIENT_SECRET

    url = "https://id.twitch.tv/oauth2/token"
    data = urllib.parse.urlencode({
                                    'grant_type' : 'refresh_token',
                                    'refresh_token' : config.CLIENT_REFRESH_TOKEN,
                                    'client_id' : config.CLIENT_ID,
                                    'client_secret' : config.CLIENT_SECRET                                    
                                    })

    data = data.encode('utf-8')
#    utility.print_toscreen(url)
    req = urllib.request.Request(url)


    try: 
	    response = urllib.request.urlopen(req, data = data)
    
    except (HTTPError, URLError) as err:
       utility.print_toscreen("HTTP Error" + str(err))
       
       utility.restart()

    
    data = json.load(response)   
    
    global access_token
    access_token = data["access_token"]
    
#    utility.print_toscreen(data)
#    utility.print_toscreen(data["access_token"])

    return data["access_token"]
    


def get_channel_id(channel_name):

    url = "https://api.twitch.tv/kraken/users/?api_version=5&client_id=" + config.CLIENT_ID + "&login=" + channel_name
#    utility.print_toscreen(url)
    req = urllib.request.Request(url)

    response = urllib.request.urlopen(req)
    data = json.load(response)   
#    utility.print_toscreen(data)
#    utility.print_toscreen(data["access_token"])

    return data["users"][0]["_id"]    



def is_there_clip(clip_id):

    
    url = "https://api.twitch.tv/helix/clips?id=" + clip_id

    
    req = urllib.request.Request(url,
                  headers = {
                    "Client-ID": config.CLIENT_ID ,
                    "Authorization": "Bearer " + access_token ,
                    },
                      data = None)
                      
    try:                      
        response = urllib.request.urlopen(req)
    except (HTTPError, URLError) as err:
        utility.print_toscreen("HTTP Error" + str(err))
        utility.restart()

    data = json.load(response)   
#    utility.print_toscreen(data)
    
    try:
        result = data["data"][0]["id"]
    
    except IndexError:
#        utility.print_toscreen("false")
        return False
    
 #   utility.print_toscreen("true")
    return True



def create_clip(channel_id):

    url = "https://api.twitch.tv/helix/clips"
    data = urllib.parse.urlencode({
                                    'has_delay' : 'true',
                                    'broadcaster_id' : channel_id,
                                    })
    data = data.encode('utf-8')

    req = urllib.request.Request(url,
                  headers = {
                    "Client-ID": config.CLIENT_ID,
                    "Authorization": "Bearer " + access_token ,
                    }, data = data)

    try:
        response = urllib.request.urlopen(req,data)    
    
    except (HTTPError, URLError) as err:
       utility.print_toscreen("HTTP Error" + str(err))
       return 0

    
    data = json.load(response)   
#    utility.print_toscreen(str(data))
    
    return data["data"][0]["id"]
    
 
def is_stream_live(channel_id):
	
    url = "https://api.twitch.tv/helix/streams?user_id=" + channel_id
    
    utility.print_toscreen(url)
	
    req = urllib.request.Request(url,
                  headers = {
                    "Client-ID": config.CLIENT_ID ,
                      "Authorization": "Bearer " + access_token,
                  },
                      data=None)
                      
    response = urllib.request.urlopen(req)
    data = json.load(response)   
#    utility.print_toscreen(data)
    
    try:
        result = data["data"][0]["type"]
#       utility.print_toscreen(resulqt)
    
    except IndexError:
#	  	utility.print_toscreen("false")
        return False
    
#    utility.print_toscreen("true")
    return True

	
	



def test():
     

    channel_id = get_channel_id("summit1g") 
    utility.print_toscreen(channel_id)

    create_clip (channel_id)

#    utility.print_toscreen(is_stream_live("159319477"))
            
#    auth()
#    access_token = get_access_token()
#    utility.print_toscreen(access_token)


utility.print_toscreen("Starting Twitch API")
get_access_token() 
utility.print_toscreen(access_token)
utility.print_toscreen("Token Refreshed")

myThread = threading.Timer(3600, do_refresh_token)  
myThread.start()


if __name__ == "__main__":
    utility.print_toscreen("Hello")
    test()
	
