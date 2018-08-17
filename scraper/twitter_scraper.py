#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thurs Aug 16 2018

"""

from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json

#declare variables
# consumer key and consumer secret key you get from twitter when you create
# .. a new app at http://apps.twitter.com
ckey = "CONSUMER_KEY"
csecret = "CONSUMER_SECRET"

# access token and access secret key you get from twitter when you create 
# .. a new app at http://apps.twitter.com
atoken = "ACCESS_TOKEN"
asecret = "ACCESS_SECRET"

class listener(StreamListener):

            
    def on_data(self, data):
        all_data = json.loads(data)
        
        tweet = all_data["text"]
        
        username = all_data["user"]["created_at"]
        
        

        print((username,tweet))
        
        return True
    
    def on_error(self, status_code):
        if status_code == 420:
            print('You are about to hit a RateLimit Exception.\n Disconnecting from server...')
            return False
 
 
if __name__ == '__main__': # twitter authentification & connection to Twitter Streaming AP

  auth = OAuthHandler(ckey, csecret)
  auth.set_access_token(atoken, asecret)

  twitterStream = Stream(auth, listener())
  
  #filter tweets to capture data by keywords
  twitterStream.filter(track=['#cowboys'])
