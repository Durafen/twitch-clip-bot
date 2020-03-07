import urllib2
import json
import threading

import utility
import config





access_token  = ""


def do_refresh_token():
	
    get_access_token() 
    print "Token Refreshed"
    print access_token

    myThread.run()	
	
	

def get_access_token_bad():

    status = "Yay"
    url = "https://id.twitch.tv/oauth2/token?client_id=" + config.CLIENT_ID + "&client_secret="  + config.CLIENT_SECRET + "&grant_type=client_credentials&scope=clips:edit"
    
    print url
    
    req = urllib2.Request(url,data = '{"message":{"body":'+ status +'}}')

    response = urllib2.urlopen(req)
    data = json.load(response)   
    
    print data
    return data["access_token"]
    

def auth():

    status = "Yay"
    url = "https://id.twitch.tv/oauth2/token?client_id=" + config.CLIENT_ID + "&client_secret="  + config.CLIENT_SECRET + "&code=lv1tcwmo8gidqzkj2ipk62po8evg16&grant_type=authorization_code&redirect_uri=http://localhost"
    
#    print url
    
    req = urllib2.Request(url,data = '{"message":{"body":'+ status +'}}')

    response = urllib2.urlopen(req)
    data = json.load(response)   
    print (data)


def get_access_token():

    status = "Yay"
    url = "https://id.twitch.tv/oauth2/token?grant_type=refresh_token&refresh_token=" + config.CLIENT_REFRESH_TOKEN + "&client_id=" + config.CLIENT_ID + "&client_secret=" + config.CLIENT_SECRET
#    print url
    req = urllib2.Request(url,data = '{"message":{"body":'+ status +'}}')


    try:
	    response = urllib2.urlopen(req)
    
    except urllib2.HTTPError, err:
       print "HTTP Error", err.code
       utility.restart()

    except urllib2.URLError, err:
       print "URL error:", err.reason
       utility.restart()
    
    
    data = json.load(response)   
    
    global access_token
    access_token = data["access_token"]
    
#    print data
#    print data["access_token"]

    return data["access_token"]
    


def get_channel_id(channel_name):

    status = "Yay"
    url = "https://api.twitch.tv/kraken/users/?api_version=5&client_id=" + config.CLIENT_ID + "&login=" + channel_name
#    print url
    req = urllib2.Request(url)

    response = urllib2.urlopen(req)
    data = json.load(response)   
#    print data
#    print data["access_token"]

    return data["users"][0]["_id"]
    



def is_there_clip(clip_id):

    status = "Yay"
    url = "https://api.twitch.tv/helix/clips?id=" + clip_id

    
    req = urllib2.Request(url,
                  headers = {
                    "Client-ID": config.CLIENT_ID ,
                    },
                      data=None)
                      
    response = urllib2.urlopen(req)
    data = json.load(response)   
#    print (data)
    
    try:
        result = data["data"][0]["id"]
    
    except IndexError:
    # handle this
    	print "false"
        return False
    
    print "true"
    return True



def create_clip(channel_id):

    status = "Yay"
    req = urllib2.Request("https://api.twitch.tv/helix/clips?has_delay=true&broadcaster_id=" + channel_id,
                  headers = {
                    "Authorization": "Bearer " + access_token ,
                    },
                      data = '{"message":{"body":'+ status +'}}')


    try:
        response = urllib2.urlopen(req)    
    
    except urllib2.HTTPError, err:
       print "HTTP Error", err.code
       return 0

    except urllib2.URLError, err:
       print "URL error:", err.reason
       return 0
    
    
    data = json.load(response)   
    print (data)
    
    return data["data"][0]["id"]
    
 
def is_stream_live(channel_id):
	
    url = "https://api.twitch.tv/helix/streams?user_id=" + channel_id
    
    print url
	
    req = urllib2.Request(url,
                  headers = {
                    "Client-ID": config.CLIENT_ID ,
                    },
                      data=None)
                      
    response = urllib2.urlopen(req)
    data = json.load(response)   
#    print (data)
    
    try:
        result = data["data"][0]["type"]
#       print result
    
    except IndexError:
    # handle this
#	  	print "false"
        return False
    
#    print "true"
    return True

	
	



def test():
     

#    channel_id = get_channel_id("onwardmasterleague")
#    print channel_id

    print is_stream_live("159319477")
    
    
#    access_token = get_access_token()
#    print access_token
    
#    clip_id = create_clip(access_token, channel_id)
#    clip_url = "https://clips.twitch.tv/" + clip_id
#    print (clip_url)
    
#    auth()
#    access_token = get_access_token()
#    print access_token


#    print is_there_clip("BenevolentAttractiveLarkAMPTropPunch")



print "Starting Twitch API"
get_access_token() 
print access_token
print "Token Refreshed"

myThread = threading.Timer(3600, do_refresh_token)  # timer is set to 3 seconds
myThread.start()



if __name__ == "__main__":
	test()
	
	
	



