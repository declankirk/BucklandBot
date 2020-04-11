#!/usr/bin/env python
# encoding: utf-8

# Modified from https://gist.github.com/yanofsky/5436496

import tweepy #https://github.com/tweepy/tweepy
#import csv
import re

from config import consumer_key, consumer_secret, access_key, access_secret


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print("...%s tweets downloaded so far" % (len(alltweets)))
	
	f = open("tweets.txt","wb")

	for tweet in alltweets:
		tweetstring = tweet.text
		if tweetstring.startswith("RT"): continue # ignore retweets

		tweetstring = re.sub(r"http\S+", "", tweetstring) # getting rid of links
		tweetstring = re.sub(r"@\S+", "", tweetstring) # so we don't @ people
		tweetstring = re.sub(r".*…", "", tweetstring) # remove quotes of replied tweets

		tweetstring = re.sub(r"&amp;", "&", tweetstring)
		tweetstring = re.sub(r"&gt;", ">", tweetstring)
		
		tweetstring += '\n'
		f.write(tweetstring.encode("utf-8"))
	f.close()
	pass

if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("ProfBuckland")