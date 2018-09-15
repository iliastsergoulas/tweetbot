# This is a bot created to tweet posts of www.agristats.eu in a specific schedule
# The code is available under MIT license, as stipulated in https://github.com/iliastsergoulas/tweetbot/blob/master/LICENSE.
# Author: Ilias Tsergoulas

import tweepy
import time, os
import pandas as pd
import random
import csv
import datetime
import sqlalchemy as sa
import requests

# Setting credentials for Twitter account
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True) #Active wait on rate limit

argfile="Exported_Data.txt"
# Retrieving the first 50 tweets from the timeline of the main agricultural press's users
rdmTweets1 = api.user_timeline(screen_name = 'ypaithros', count = 40, include_rts = False)
rdmTweets2 = api.user_timeline(screen_name = 'Agronewsgr', count = 40, include_rts = False)
rdmTweets3 = api.user_timeline(screen_name = 'agrocapital', count = 40, include_rts = False)
rdmTweets4 = api.user_timeline(screen_name = 'agrotikanew', count = 40, include_rts = False)
rdmTweets5 = api.user_timeline(screen_name = 'agro24gr', count = 40, include_rts = False)
rdmTweets6 = api.user_timeline(screen_name = 'DaniNierenberg', count = 40, include_rts = False)
rdmTweets7 = api.user_timeline(screen_name = 'FAOnews', count = 40, include_rts = False)
rdmTweets8 = api.user_timeline(screen_name = 'FarmingFutures', count = 40, include_rts = False)
rdmTweets9 = api.user_timeline(screen_name = 'EU_Agri', count = 40, include_rts = False)
rdmTweets10 = api.user_timeline(screen_name = 'WBG_Agriculture', count = 40, include_rts = False)

if __name__ == "__main__":
    followers = api.followers_ids("agristatseu")
    friends = api.friends_ids("agristatseu")
    for f in friends:
        if f not in followers:
            api.destroy_friendship(f)
            print "Unfollowed".format(api.get_user(f).screen_name)
    while True:
        tweets_gr=[]
        tweets_en=[]
        for tweet in rdmTweets1:
            tweets_gr.append(tweet.text)
        for tweet in rdmTweets2:
            tweets_gr.append(tweet.text)
        for tweet in rdmTweets3:
            tweets_gr.append(tweet.text)
        for tweet in rdmTweets4:
            tweets_gr.append(tweet.text)
        for tweet in rdmTweets5:
            tweets_gr.append(tweet.text)
        for tweet in rdmTweets6:
            tweets_en.append(tweet.text)
        for tweet in rdmTweets7:
            tweets_en.append(tweet.text)
        for tweet in rdmTweets8:
            tweets_en.append(tweet.text)
        for tweet in rdmTweets9:
            tweets_en.append(tweet.text)
        for tweet in rdmTweets10:
            tweets_en.append(tweet.text)
        #.encode('utf-8')
        con = sa.create_engine('postgresql+psycopg2://user:password@host/database', encoding = 'utf-8')
        tweets_gr = pd.DataFrame(tweets_gr)
        tweets_gr.to_sql('tweets_gr', con, if_exists='replace')
        tweets_en = pd.DataFrame(tweets_en)
        tweets_en.to_sql('tweets_en', con, if_exists='replace')
        # Choosing posts to tweet and tweeting
        with open(argfile) as f:
            myposts = csv.reader(f, delimiter=',')
            myposts=pd.DataFrame(list(myposts))
            i=random.sample(list(myposts.index), 1)[0] # Pick a random post
            tweet = "%s %s #agriculture #agristats #data #farming #farmers #agricultural" % (myposts.iat[i,0],myposts.iat[i,1])
            api.update_status(tweet) # Tweeting
            #status = fbapi.put_wall_post(tweet)
            myrand=random.randint(0, 22)
            if myrand==1:
                tweet = "Get #reports, #statistics, #data, #infographics and #maps about #agriculture #agristats #farming #agricultural #SmartFarming #datascience www.agristats.eu"
                try:
                    api.update_status(tweet) # Tweeting
                except tweepy.TweepError as e:
                    print(e.reason)
            if myrand==2:
                tweet = "Check our collection of #infographics and #maps ! #agriculture #agristats #farmers #farming #agricultural #SmartFarming #research http://www.agristats.eu/en/reports-tools/infographics/ #datascience"
                try:
                    api.update_status(tweet) # Tweeting
                except tweepy.TweepError as e:
                    print(e.reason)
            if myrand==3:
                tweet = "Looking for open data in agriculture? Subscribe to our newsletter and get a free catalog of open data sources #agristats #farming #farmers #agricultural #SmartFarming #research #datascience http://www.agristats.eu/en/newsletter-subscription-form/"
                try:
                    api.update_status(tweet) # Tweeting
                except tweepy.TweepError as e:
                    print(e.reason)
            if myrand==4:
                tweet = "View our online applications for #agriculture #agristats #farmers #agricultural #farming #SmartFarming http://www.agristats.eu/en/reports-tools/applications/ #research #datascience"
                try:
                    api.update_status(tweet) # Tweeting
                except tweepy.TweepError as e:
                    print(e.reason)
            if myrand==5:
                tweet = "All #agristats applications are open and the code is available in GitHub https://github.com/iliastsergoulas #agriculture #agristats #farming #farmers #agricultural #SmartFarming #research #datascience"
                try:
                    api.update_status(tweet) # Tweeting
                except tweepy.TweepError as e:
                    print(e.reason)
            if myrand==6:
                tweet = "Take a look at our #surveys and help us by participating in one of them easily and quickly http://www.agristats.eu/en/surveys/ #agriculture #farming #agristats #SmartFarming #farmers #agricultural #datascience"
                try:
                    api.update_status(tweet) # Tweeting
                except tweepy.TweepError as e:
                    print(e.reason)
            if myrand==7:
                tweet = "Join us in Facebook. Our page is https://www.facebook.com/Agristats-1414824828586626/ #agriculture #agristats #farmers #agricultural #farming #SmartFarming #research #datascience"
                try:
                    api.update_status(tweet) # Tweeting
                except tweepy.TweepError as e:
                    print(e.reason)
            if myrand==8:
                tweet = "Looking to taste Greek wine again? Ever heard about ouzo, tsipouro or raki and wished you had some more? Visit http://mikk.ro/BPNH and get your preference. #agriculture #agristats #farmers #wine #farming #SmartFarming"
                try:
                    api.update_status(tweet) # Tweeting
                except tweepy.TweepError as e:
                    print(e.reason)
            if myrand==9:
                tweet = "Crete is an island holding a treasure of local products. Food, wine, spirits and natural products for you by visiting http://mikk.ro/BPNK #agriculture #agristats #farmers #crete #greece #farming #SmartFarming"
                try:
                    api.update_status(tweet) # Tweeting
                except tweepy.TweepError as e:
                    print(e.reason)
            if myrand==10:
                tweet = "2300 authentic #local products from more than 180 small producers from every corner of #Greece. Visit http://mikk.ro/BPNM to admire the wide variety #agriculture #agristats #farmers #farming #SmartFarming"
                try:
                    api.update_status(tweet) # Tweeting
                except tweepy.TweepError as e:
                    print(e.reason)
            if myrand==11:
                filename = 'temp.png'
                request = requests.get("http://88.99.13.199:3838/shinyapps/wordcloud/twitterclouden.png", stream=True)
                if request.status_code == 200:
                    with open(filename, 'wb') as image:
                        for chunk in request:
                            image.write(chunk)
                    try:
                        api.update_with_media(filename,status="Top stories in agriculture via Twitter www.agristats.eu")
                        os.remove(filename)
                    except tweepy.TweepError as e:
                        print(e.reason)
            if myrand==12:
                tweet = "If you want to learn more about R and create fascinating data analysis applications, take a look at this course 'R Programming For Beginners' https://bit.ly/2LSkScF #agriculture #agristats #farmers #farming #SmartFarming #research #datascience #statistics"
                try:
                    api.update_status(tweet) # Tweeting
                except tweepy.TweepError as e:
                    print(e.reason)
            for tweet in tweepy.Cursor(api.search, q='#agriculture').items():
                try:
                    tweet.favorite()
                    # Follow the user who tweeted
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
            for tweet in tweepy.Cursor(api.search, q='#farming').items():
                try:
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
            for tweet in tweepy.Cursor(api.search, q='#smartfarming').items():
                try:
                    tweet.favorite()
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
            for tweet in tweepy.Cursor(api.search, q='#rural').items():
                try:
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
        time.sleep(3600) # The time interval between tweets is one hour.
