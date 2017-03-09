import markovify
import configparser
import twitter
import os
import json

def connection_init():

	cfg = configparser.ConfigParser()
	cfg.read('config.ini')

	ACCESS_TOKEN = cfg.get('twitter', 'ACCESS_TOKEN') 
	ACCESS_SECRET = cfg.get('twitter', 'ACCESS_SECRET')
	CONSUMER_KEY = cfg.get('twitter', 'CONSUMER_KEY') 
	CONSUMER_SECRET = cfg.get('twitter', 'CONSUMER_SECRET')

	oauth = twitter.oauth.OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
	# Initiate the connection to Twitter REST API
	twitter_api = twitter.Twitter(auth=oauth)

	return twitter_api

def getAllTweets():

	twitter_api = connection_init()

	# get initial 50
	all_tweets = []
	statuses = twitter_api.statuses.user_timeline(screen_name='CptKrrk', count=50, include_retweets=True )
	all_tweets = all_tweets + statuses
	results = len(statuses)
	index = 0
	while results >= 50:
		statuses = twitter_api.statuses.user_timeline(screen_name='CptKrrk', count=50, include_retweets=True, max_id=statuses[49]['id'])
		all_tweets = all_tweets + statuses
		results = len(statuses)
		print( index )
		index = index + 1

	all_tweets = sorted(all_tweets,key=lambda l:l['id'], reverse=False)

	return all_tweets

def storeItems( json_content, itemType ):

	with open( os.getcwd() + '/tweets/' + itemType + 'DB.json', 'w' ) as DB_file:
		DB_file.write( json.dumps(json_content, indent=2) )

def consolidate( content_list, itemType, verbose=True ):

	all_content = getDatabase( itemType )
	if( verbose ):
		print( str(len( all_content )) + " " + itemType + " in DB to start" )

	for content_json in content_list:
		for item in content_json:
			if item not in all_content:
			
				all_content.append( item )
			
	if( verbose ):
		print( str(len( all_content )) + " " + itemType + " now in DB" )

	return all_content

def getDatabase( itemType ):

	with open( os.getcwd() + '/tweets/' + itemType + 'DB.json' ) as json_data:
		all_content = json.load(json_data)
		json_data.close()

	return all_content

def getMentions():

	mentions_json = []

	twitter_api = connection_init()
	mentions = twitter_api.statuses.mentions_timeline()

	for mention in mentions:
		if( mention['text'] is not None and mention['id'] is not None):
			mention_json = { 	'id' : mention['id'], 
								'text' : mention['text'], 
								'created_at' : mention['created_at'], 
								'screen_name' : mention['user']['screen_name']
							}
			mentions_json.append( mention_json )

	return mentions_json

def refreshMentions():

	mentions = getMentions()

	mentions = consolidate( [mentions], 'mentions' )

	storeItems( mentions, 'mentions' )

def refreshItems( itemType ):

	if( itemType == 'tweets' ):
		items = getAllTweets()
	elif( itemType == 'mentions' ):
		items = getMentions()

	items = consolidate( [items], itemType )

	storeItems( items, itemType )

