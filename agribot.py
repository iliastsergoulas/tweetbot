#!/usr/bin/env python
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
import pytumblr
import feedparser
import praw
from datetime import date

# Setting credentials for Tumblr account
t = pytumblr.TumblrRestClient(
    '',
    '',
    '',
    ''
)
# Setting credentials for Twitter account agristats
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_KEY = ''
ACCESS_SECRET = ''
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True) #Active wait on rate limit
# Setting credentials for Twitter account wineroutes
CONSUMER_KEY_WINE = ''
CONSUMER_SECRET_WINE = ''
ACCESS_KEY_WINE = ''
ACCESS_SECRET_WINE = ''
auth_WINE = tweepy.OAuthHandler(CONSUMER_KEY_WINE, CONSUMER_SECRET_WINE)
auth_WINE.set_access_token(ACCESS_KEY_WINE, ACCESS_SECRET_WINE)
api_WINE = tweepy.API(auth_WINE, wait_on_rate_limit=True) #Active wait on rate limit
blogName = ''
wineblogName = ''
mywineposts=pd.read_csv("wineroutes.csv",sep=",")
j=0
reddit = praw.Reddit(client_id='', client_secret="",
                     password='', user_agent='',
                     username='')

postsfile="Exported_Data.txt"
myaffiliates=pd.read_csv("affiliates.csv",sep=",")

def tweetimage(url, status):
    filename = 'temp.png'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)
        try:
            api_WINE.update_with_media(filename, status=status)
            os.remove(filename)
        except tweepy.TweepError as e:
            print(e.reason)

def rsspost(url, filename, account):
    id_file = filename
    feed = feedparser.parse(url)
    #       Read the last id
    with open(id_file,'r') as file_:
        last_id = file_.read().strip()
    most_recent_id = feed['entries'][0]['id']
    if (last_id == most_recent_id):
        # Do nothing
        print "None available"
    else:
        # Save the new ID for later
        with open(id_file, 'w') as file_:
            file_.write(most_recent_id)
        # Loop through the posts
        i=0
        for post in feed['entries']:
            if i<1:
                # If the post has been encountered before, time to end things.
                if (last_id == post["id"]):
                    print "All done"
                else:
                    if (account=="wineroutes"):
                        tweet = "#wine #winelovers #winelover #winery #travel #wineroutes " + post["link"]
                        try:
                            api_WINE.update_status(tweet)
                            # Queue it on Tumblr
                            try:
                                print post["media_thumbnail"][0]["url"]
                                try:
                                    print t.create_link(wineblogName, title=post["title"].encode("utf-8"), url=post["link"],
                                                        thumbnail=post["media_thumbnail"][0]["url"],
                                                        description=post["summary"].encode("utf-8"), tweet='[]',
                                                        tags=['wineroutes', 'wine', 'winetasting', 'winelover', 'winery',
                                                              'agristats'])
                                except:
                                    print "failed to create link post"
                            except:
                                print "No thumbnail"
                                try:
                                    print t.create_link(blogName, title=post["title"].encode("utf-8"), url=post["link"],
                                                        description=post["summary"].encode("utf-8"), tweet='[]',
                                                        state="queue",
                                                        tags=['wineroutes', 'wine', 'winetasting', 'winelover',
                                                              'winery','agristats'])
                                except:
                                    print "failed to create link post"
                            try:
                                reddit.subreddit('wineroutes').submit(title=post["title"].encode("utf-8"), url=post["link"],selftext=post["summary"].encode("utf-8"))
                            except Exception as e:
                                print e
                                print "failed to post on Reddit"
                        except:
                            print "Duplicate post"
                    else:
                        tweet = "#agriculture #agristats #farming #agricultural #SmartFarming "+post["link"]
                        try:
                            api.update_status(tweet)
                            # Queue it on Tumblr
                            try:
                                print post["media_thumbnail"][0]["url"]
                                try:
                                    print t.create_link(blogName, title=post["title"].encode("utf-8"), url=post["link"],
                                                        thumbnail=post["media_thumbnail"][0]["url"],
                                                        description=post["summary"].encode("utf-8"), tweet='[]',
                                                        tags=['agristats', 'agriculture', 'farming', 'farmer', 'rural',
                                                              'science'])
                                except:
                                    print "failed to create link post"
                            except:
                                print "No thumbnail"
                                try:
                                    print t.create_link(blogName, title=post["title"].encode("utf-8"), url=post["link"],
                                                        description=post["summary"].encode("utf-8"), tweet='[]',
                                                        state="queue",
                                                        tags=['agristats', 'agriculture', 'farming', 'farmer', 'rural',
                                                              'science'])
                                except:
                                    print "failed to create link post"
                        except:
                            print "Duplicate post"
                i=1

if __name__ == "__main__":
    #followers = api.followers_ids("agristatseu")
    #friends = api.friends_ids("agristatseu")
    #for f in friends:
        #if f not in followers:
            #api.destroy_friendship(f)
            #print "Unfollowed".format(api.get_user(f).screen_name)
    while True:
        # Choosing posts to tweet and tweeting
        myrand=random.randint(1, 69)
        if myrand==6:
            tweet = "If you want to learn more about creating fascinating data analysis applications, take a look at this list of courses https://bit.ly/2xNIBSR #agriculture #agristats #farmers #farming #SmartFarming #research #datascience #statistics"
            try:
                api.update_status(tweet) # Tweeting
                try:
                    print t.create_link(blogName, title="If you want to learn more about creating fascinating data analysis applications, take a look at this list of courses",
                        tags=['agristats','agriculture','farming','farmer','rural','datascience'],
                        url="https://bit.ly/2xNIBSR",thumbnail="https://www.simplilearn.com/ice9/free_resources_article_thumb/Data-Science-vs.-Big-Data-vs.jpg")
                except:
                    print "failed to create link post"
            except tweepy.TweepError as e:
                print(e.reason)
        if 1 <= myrand <= 11:
            rsspost('https://ec.europa.eu/research/rss/whatsnew-1.xml','europa.txt',"agristats")
        if 12 <= myrand <= 15:
            rsspost('http://www.theconsciousfarmer.com/feed/','consciousfarmer.txt',"agristats")
        if 16 <= myrand <= 19:
            rsspost('http://www.fao.org/news/en/?no_cache=1&feed_id=16872&type=334','fao.txt',"agristats")
        if 20 <= myrand <= 23:
            rsspost('https://www.sciencedaily.com/rss/plants_animals/agriculture_and_food.xml','sciencedaily.txt',"agristats")
        if 24 <= myrand <= 27:
            rsspost('http://feeds.feedburner.com/CivilEats','civileats.txt',"agristats")
        if 28 <= myrand <= 31:
            rsspost('https://modernfarmer.com/feed/','modernfarmer.txt',"agristats")
        if 32 <= myrand <= 35:
            rsspost('https://ucanr.edu/blogs/food/rssmain.xml','foodblog.txt',"agristats")
        if 36 <= myrand <= 45:
            rsspost('https://www.youtube.com/feeds/videos.xml?user=Ryanfun1','ryanfun1.txt',"agristats")
        if 46 <= myrand <= 49:
            rsspost('http://europa.eu/rapid/search-result.htm?query=42&language=EN&format=RSS','euagri.txt',"agristats")
        if 50 <= myrand <= 53:
            for tweet in tweepy.Cursor(api.search, q='#agriculture').items():
                try:
                    tweet.favorite()
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
        if 54 <= myrand <= 57:
            for tweet in tweepy.Cursor(api.search, q='#farming').items():
                try:
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
        if 58 <= myrand <= 61:
            for tweet in tweepy.Cursor(api.search, q='#smartfarming').items():
                try:
                    tweet.favorite()
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
        if 62 <= myrand <= 65:
            for tweet in tweepy.Cursor(api.search, q='#rural').items():
                try:
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
        if 66 <= myrand <= 69:
            rsspost('https://www.youtube.com/feeds/videos.xml?channel_id=UC3q5NWsebP9NFfBsxJGvcEA','farminglife.txt',"agristats")
        time.sleep(200)
        # Choosing posts to tweet at winerouteseu
        myrand = random.randint(1, 242)
        if 1 <= myrand <= 2:
            tweetimage("http://wineroutes.eu/images/routesimages/argolida.png","Check out the Wine Route of Argolida in Greece. More routes and wineries through our Android app Wine Routes https://bit.ly/2Hwc6hx #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel")
        if myrand == 3:
            tweetimage("http://wineroutes.eu/images/routesimages/arkadia.png","Check out the Wine Route of Arkadia in Greece. More routes and wineries through our Android app Wine Routes https://bit.ly/2Hwc6hx #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel")
        if myrand == 4:
            tweetimage("http://wineroutes.eu/images/routesimages/attiki.png","Check out the Wine Route of Attiki in Greece. More routes and wineries through our Android app Wine Routes https://bit.ly/2Hwc6hx #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel")
        if myrand == 5:
            tweetimage("http://wineroutes.eu/images/routesimages/chalkidiki.png","Check out the Wine Route of Chalkidiki in Greece. More routes and wineries through our Android app Wine Routes https://bit.ly/2Hwc6hx #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel")
        if myrand == 6:
            tweetimage("http://wineroutes.eu/images/routesimages/dionysus.png","Check out the Wine Route of Dionysus in Greece. More routes and wineries through our Android app Wine Routes https://bit.ly/2Hwc6hx #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel")
        if myrand == 7:
            tweetimage("http://wineroutes.eu/images/routesimages/epirus.png","Check out the Wine Route of Epirus in Greece. More routes and wineries through our Android app Wine Routes https://bit.ly/2Hwc6hx #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel")
        if myrand == 8:
            tweetimage("http://wineroutes.eu/images/routesimages/goumenissa.png","Check out the Wine Route of Goumenissa in Greece. More routes and wineries through our Android app Wine Routes https://bit.ly/2Hwc6hx #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel")
        if myrand == 9:
            tweetimage("http://wineroutes.eu/images/routesimages/ilia.png","Check out the Wine Route of Ilia in Greece. More routes and wineries through our Android app Wine Routes https://bit.ly/2Hwc6hx #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel")
        if myrand == 10:
            tweetimage("http://wineroutes.eu/images/routesimages/kos.png","Check out the Wine Route of Kos in Greece. More routes and wineries through our Android app Wine Routes https://bit.ly/2Hwc6hx #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel")
        if myrand == 11:
            tweetimage("http://wineroutes.eu/images/routesimages/lakes.png","Check out the Wine Route of Lakes in Greece. More routes and wineries through our Android app Wine Routes https://bit.ly/2Hwc6hx #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel")
        if myrand == 12:
            tweetimage("http://wineroutes.eu/images/routesimages/lakonia.png","Check out the Wine Route of Lakonia in Greece. More routes and wineries through our Android app Wine Routes https://bit.ly/2Hwc6hx #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel")
        if myrand == 13:
            tweetimage("http://wineroutes.eu/images/routesimages/naousa.png","Check out the Wine Route of Naousa in Greece. More routes and wineries through our Android app Wine Routes https://bit.ly/2Hwc6hx #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel")
        if myrand == 14:
            tweetimage("http://wineroutes.eu/images/routesimages/olympus.png","Check out the Wine Route of Olympus in Greece. More routes and wineries through our Android app Wine Routes https://bit.ly/2Hwc6hx #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel")
        if myrand == 15:
            tweetimage("http://wineroutes.eu/images/routesimages/rhodes.png","Check out the Wine Route of Rhodes in Greece. More routes and wineries through our Android app Wine Routes https://bit.ly/2Hwc6hx #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel")
        if myrand == 16:
            tweetimage("http://wineroutes.eu/images/routesimages/thessaloniki.png","Check out the Wine Route of Thessaloniki in Greece. More routes and wineries through our Android app Wine Routes https://bit.ly/2Hwc6hx #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel")
        if 17 <= myrand <= 27:
            for tweet in tweepy.Cursor(api_WINE.search, q='#winelover').items():
                try:
                    tweet.favorite()
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
        if 28 <= myrand <= 38:
            tweet = "Are you a winemaker? You can now register your winery at Wine Routes and manage your winery's page for thousands of app users. Just visit https://bit.ly/2XiGWQI #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel"
            try:
                api_WINE.update_status(tweet)  # Tweeting
            except tweepy.TweepError as e:
                print(e.reason)
        if 39 <= myrand <= 54:
            for tweet in tweepy.Cursor(api_WINE.search, q='#winetasting').items():
                try:
                    tweet.favorite()
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
        if 55 <= myrand <= 65:
            for tweet in tweepy.Cursor(api_WINE.search, q='#winery').items():
                try:
                    tweet.favorite()
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
        if 66 <= myrand <= 70:
            for tweet in tweepy.Cursor(api_WINE.search, q='#winetime').items():
                try:
                    tweet.favorite()
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
        if 71 <= myrand <= 91:
            tweet = "Wine Routes: Our Android app about over 10k wineries across the world. Download it and join a community of wine lovers. https://bit.ly/2tMDG29 #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel"
            try:
                api_WINE.update_status(tweet) # Tweeting
            except tweepy.TweepError as e:
                print(e.reason)
        if 92 <= myrand <= 102:
            for tweet in tweepy.Cursor(api_WINE.search, q='#wineexplorer').items():
                try:
                    tweet.favorite()
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
        if 103 <= myrand <= 113:
            for tweet in tweepy.Cursor(api_WINE.search, q='#vineyard').items():
                try:
                    tweet.favorite()
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
        if myrand==114:
            tweet = "Join us in Facebook. Our page is https://www.facebook.com/Agristats-1414824828586626/ #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel"
            try:
                api_WINE.update_status(tweet) # Tweeting
            except tweepy.TweepError as e:
                print(e.reason)
        if myrand==115:
            tweet = "Join our community in Reddit at https://www.reddit.com/r/wineroutes/ and exchange opinions with fellow #wine #cheers #wineroutes #agristats #winetasting #winelover #wineries #vino #travel"
            try:
                api_WINE.update_status(tweet) # Tweeting
            except tweepy.TweepError as e:
                print(e.reason)
        if 116 <= myrand <= 126:
            for tweet in tweepy.Cursor(api_WINE.search, q='#winetasting').items():
                try:
                    tweet.favorite()
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
        if 127 <= myrand <= 137:
            for tweet in tweepy.Cursor(api_WINE.search, q='#wineoclock').items():
                try:
                    tweet.favorite()
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
        if 138 <= myrand <= 148:
            for tweet in tweepy.Cursor(api_WINE.search, q='#winery').items():
                try:
                    tweet.favorite()
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
        if 149 <= myrand <= 159:
            for tweet in tweepy.Cursor(api_WINE.search, q='#winetime').items():
                try:
                    tweet.favorite()
                    tweet.user.follow()
                    break
                except tweepy.TweepError as e:
                    print(e.reason)
        if 160 <= myrand <= 180:
            rsspost('https://www.wine-searcher.com/rss-feed/dept/wine+news','winenews.txt', "wineroutes")
        if 181 <= myrand <= 201:
            rsspost('https://wineeconomist.com/feed/','wineeconomist.txt', "wineroutes")
        if 202 <= myrand <= 222:
            rsspost('http://winefolly.com/feed/','winefolly.txt', "wineroutes")
        if 203 <= myrand <= 210:
            tweetimage("https://i.udemycdn.com/course/480x270/207468_236e_6.jpg","Staying home? How about learning more about wine online? More at https://bit.ly/33IvhxO #wine #cheers #wineroutes #winetasting #winelover #wineries #vino")
            try:
                print t.create_link(wineblogName, title="Staying home? How about learning more about wine online?", url="https://bit.ly/33IvhxO",
                              thumbnail="https://i.udemycdn.com/course/480x270/207468_236e_6.jpg",
                              tags=['wineroutes', 'wine', 'winetasting', 'winelover', 'winery','agristats'])
            except:
                print "failed to create link post"
        if 211 <= myrand <= 218:
            tweetimage("https://i.udemycdn.com/course/480x270/471052_601d_2.jpg","Staying home? How about learning more about wine online? More at https://bit.ly/2WDE9n7 #wine #cheers #wineroutes #winetasting #winelover #wineries #vino")
            try:
                print t.create_link(wineblogName, title="Staying home? How about learning more about wine online?",
                              url="https://bit.ly/2WDE9n7",thumbnail="https://i.udemycdn.com/course/480x270/471052_601d_2.jpg",
                              tags=['wineroutes', 'wine', 'winetasting', 'winelover', 'winery','agristats'])
            except:
                print "failed to create link post"
        if 219 <= myrand <= 226:
            tweetimage("https://i.udemycdn.com/course/480x270/2603922_079a.jpg","Staying home? Winemaking is a great activity! Learn more at https://bit.ly/3dsHuv0 #wine #cheers #wineroutes #winetasting #winelover #wineries #vino")
            try:
                print t.create_link(wineblogName, title="Staying home? Winemaking is a great activity!",
                              url="https://bit.ly/3dsHuv0",thumbnail="https://i.udemycdn.com/course/480x270/2603922_079a.jpg",
                              tags=['wineroutes', 'wine', 'winetasting', 'winelover', 'winery','agristats'])
            except:
                print "failed to create link post"
        if 227 <= myrand <= 234:
            tweetimage("https://i.udemycdn.com/course/480x270/98756_9bc7_5.jpg","Staying home? Winemaking is a great activity! Learn more at https://bit.ly/2xrNGCU #wine #cheers #wineroutes #winetasting #winelover #wineries #vino")
            try:
                print t.create_link(wineblogName, title="Staying home? Winemaking is a great activity!",
                              url="https://bit.ly/2xrNGCU",thumbnail="https://i.udemycdn.com/course/480x270/98756_9bc7_5.jpg",
                              tags=['wineroutes', 'wine', 'winetasting', 'winelover', 'winery','agristats'])
            except:
                print "failed to create link post"
        if 235 <= myrand <= 242:
            tweetimage("https://i.udemycdn.com/course/480x270/539300_185e_2.jpg","Staying home? Winemaking is a great activity! Learn more at https://bit.ly/3alHfjq #wine #cheers #wineroutes #winetasting #winelover #wineries #vino")
            try:
                print t.create_link(wineblogName, title="Staying home? Winemaking is a great activity!",
                              url="https://bit.ly/3alHfjq",thumbnail="https://i.udemycdn.com/course/480x270/539300_185e_2.jpg",
                              tags=['wineroutes', 'wine', 'winetasting', 'winelover', 'winery','agristats'])
            except:
                print "failed to create link post"

        
        time.sleep(7200) # The time interval between tweets is two hours.