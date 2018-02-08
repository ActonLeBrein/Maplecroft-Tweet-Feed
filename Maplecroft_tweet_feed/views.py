#-*-coding:utf-8-*-

from django.shortcuts import render
from django.conf import settings
import re
import tweepy
import csv
import json

consumer_key='z0FUyOhCqtSCXk5SiOjzYIeSU'
consumer_secret='De39tUcbRarPsn3PSZ5BgJhbve7zO4ZhmtFHmuEQsDnFGWZitW'
access_token='47037862-U38bOXgxhyzRQgTKQsMjlIejf4QUNpGBU4mgzDQPQ'
access_token_secret='3ET2WEj4RMnPvWxbURrtUngpHNZ2zMVnLu6a6TGMkuUxB'
countries_dict={}
countries_list=[]

def countries_match():
	with open(settings.BASE_DIR + '/Maplecroft_tweet_feed/countries.csv') as countries:
		csv.reader(countries,delimiter='\n')
		countries.readline()
		for country in countries:
			country=country.rstrip().split(',')
			if country[2]!='None' and country[3]!='None':
				countries_list.append(country[0].lower())
				countries_dict[country[0].lower()]=[float(country[2]),float(country[3]),country[0],country[1]]

def twitter_feed(request):
	countries_json=[]
	context = {}
	template = 'Maplecroft_tweet_feed/map.html'
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	api = tweepy.API(auth)
	if len(countries_list)==0 or len(countries_dict)==0:
		countries_match()
	number_tweets = request.GET.get('number_tweets',None)
	if number_tweets:
		public_tweets = api.user_timeline(screen_name='@MaplecroftRisk',count=number_tweets,tweet_mode='extended')
		i=1
		for tweet in public_tweets:
			if hasattr(tweet, 'retweeted_status'):
				print 'RETWEET'
				print tweet.retweeted_status.full_text
				print 'tweet number {0}'.format(i)
				print '-----------------------------------------'

				for country_list in countries_list:
					searchObj=re.search(country_list,tweet.retweeted_status.full_text,re.M|re.I)
					if searchObj:
						country_match=countries_dict[searchObj.group().lower()]
						if country_match not in countries_json:
							countries_json.append(country_match)
						else:
							pass
					else:
						pass
			else:
				print 'TWEET'
				print tweet.full_text
				print 'tweet number {0}'.format(i)
				print '-----------------------------------------'
				
				for country_list in countries_list:
					searchObj=re.search(country_list,tweet.full_text,re.M|re.I)
					if searchObj:
						country_match=countries_dict[searchObj.group().lower()]
						if country_match not in countries_json:
							countries_json.append(country_match)
						else:
							pass
					else:
						pass
			i+=1
		print countries_json, len(countries_json)
		countries_json=json.dumps(countries_json)
		context['flag']=True
		context['countries_json']=countries_json
		return render(request,template,context)
	else:
		context['flag']=False
		return render(request,template,context)