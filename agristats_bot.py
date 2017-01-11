# This is a bot created to tweet posts of www.agristats.eu in a specific schedule
# The code is available under MIT license, as stipulated in https://github.com/iliastsergoulas/tweetbot/blob/master/LICENSE.
# Author: Ilias Tsergoulas

import tweepy
import time
import pandas as pd
import random

# Setting credentials for twitter account
CONSUMER_KEY = '...'
CONSUMER_SECRET = '...'
ACCESS_KEY = '...'
ACCESS_SECRET = '...'
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
# Reading wordpress posts data
myposts=pd.read_csv("./Exported_Data.CSV")
# Choosing posts to tweet and tweeting
counter=0
while True:
    i=random.sample(myposts.index, 1)[0] # Pick a random post
    if counter!=5:
        tweet = "%s %s #%s #agriculture #data" % (myposts.iat[i,0],myposts.iat[i,1], myposts.iat[i,2])
        api.update_status(tweet) # Tweeting
    elif counter==5: # Every 5 tweets, a tweet is sent about the website
        tweet = "Get #reports, #statistics, #data, #charts, #infographics, and #maps " \
                "about #agriculture #agristats www.agristats.eu"
        api.update_status(tweet) # Tweeting
        counter=0
    counter=counter+1
    time.sleep(10800) # The time interval between tweets is three hours.
