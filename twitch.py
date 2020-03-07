#!/usr/bin/env python

import urllib.request
from urllib.parse import urlencode

from urllib.error import HTTPError, URLError

import json
import threading

import utility
import config


access_token  = ""


def do_refresh_token():
	
    get_access_token() 
    print ("Token Refreshed")
    print (access_token)

    myThread.run()	
	
	

def get_access_token_bad():


#   CHANGE TO PYTHON 3?

    status = "Yay"
    url = "https://id.twitch.tv/oauth2/token?client_id=" + config.CLIENT_ID + "&client_secret="  + config.CLIENT_SECRET + "&grant_type=client_credentials&scope=clips:edit"
    
    print (url)
    
    req = urllib.request.Request(url,data = '{"message":{"body":'+ status +'}}')

    response = urllib.request.urlopen(req)
    data = json.load(response)   
    
    print (data)
    return data["access_token"]
    

def auth():

#   CHANGE TO PYTHON 3

    status = "Yay"
    url = "https://id.twitch.tv/oauth2/token?client_id=" + config.CLIENT_ID + "&client_secret="  + config.CLIENT_SECRET + "&code=lv1tcwmo8gidqzkj2ipk62po8evg16&grant_type=authorization_code&redirect_uri=http://localhost"
    
#    print (url)
    
    req = urllib.request.Request(url,data = '{"message":{"body":'+ status +'}}')

    response = urllib.request.urlopen(req)
    data = json.load(response)   
    print (data)


def get_access_token():

    status = "Yay"
#    url = "?grant_type=refresh_token&refresh_token=" + config.CLIENT_REFRESH_TOKEN + "&client_id=" + config.CLIENT_ID + "&client_secret=" + config.CLIENT_SECRET

    url = "https://id.twitch.tv/oauth2/token"
    data = urllib.parse.urlencode({
                                    'grant_type' : 'refresh_token',
                                    'refresh_token' : config.CLIENT_REFRESH_TOKEN,
                                    'client_id' : config.CLIENT_ID,
                                    'client_secret' : config.CLIENT_SECRET                                    
                                    })

    data = data.encode('utf-8')
#    print (url)
    req = urllib.request.Request(url)


    try: 
	    response = urllib.request.urlopen(req, data = data)
    
    except (HTTPError, URLError) as err:
       print ("HTTP Error" + err.reason)
       utility.restart()


    
    data = json.load(response)   
    
    global access_token
    access_token = data["access_token"]
    
#    print (data)
#    print (data["access_token"])

    return data["access_token"]
    


def get_channel_id(channel_name):

    url = "https://api.twitch.tv/kraken/users/?api_version=5&client_id=" + config.CLIENT_ID + "&login=" + channel_name
#    print (url)
    req = urllib.request.Request(url)

    response = urllib.request.urlopen(req)
    data = json.load(response)   
#    print (data)
#    print (data["access_token"])

    return data["users"][0]["_id"]    



def is_there_clip(clip_id):

    
    url = "https://api.twitch.tv/helix/clips?id=" + clip_id

    
    req = urllib.request.Request(url,
                  headers = {
                    "Client-ID": config.CLIENT_ID ,
                    },
                      data = None)
                      
    response = urllib.request.urlopen(req)
    data = json.load(response)   
#    print (data)
    
    try:
        result = data["data"][0]["id"]
    
    except IndexError:
        print ("false")
        return False
    
    print ("true")
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
                    "Authorization": "Bearer " + access_token ,
                    }, data = data)

    try:
        response = urllib.request.urlopen(req,data)    
    
    except (HTTPError, URLError) as err:
       print ("HTTP Error" + err.reason)
       return 0

    
    data = json.load(response)   
    print (data)
    
    return data["data"][0]["id"]
    
 
def is_stream_live(channel_id):
	
    url = "https://api.twitch.tv/helix/streams?user_id=" + channel_id
    
    print (url)
	
    req = urllib.request.Request(url,
                  headers = {
                    "Client-ID": config.CLIENT_ID ,
                    },
                      data=None)
                      
    response = urllib.request.urlopen(req)
    data = json.load(response)   
#    print (data)
    
    try:
        result = data["data"][0]["type"]
#       print result
    
    except IndexError:
#	  	print "false"
        return False
    
#    print "true"
    return True

	
	



def test():
     

    channel_id = get_channel_id("summit1g") 
    print (channel_id)

    create_clip (channel_id)

#    print is_stream_live("159319477")
            
#    auth()
#    access_token = get_access_token()
#    print access_token


print ("Starting Twitch API")
get_access_token() 
print (access_token)
print ("Token Refreshed")

myThread = threading.Timer(3600, do_refresh_token)  
myThread.start()



if __name__ == "__main__":
	test()
	
	
	



