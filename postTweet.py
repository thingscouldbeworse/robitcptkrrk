import configparser
import twitter
import json
import redditGenerate
import time

def postUpdate( numUpdates=1, timebetween=0, debug=False ):

	cfg = configparser.ConfigParser()
	cfg.read('config.ini')

	ACCESS_TOKEN = cfg.get('twitter', 'ACCESS_TOKEN') 
	ACCESS_SECRET = cfg.get('twitter', 'ACCESS_SECRET')
	CONSUMER_KEY = cfg.get('twitter', 'CONSUMER_KEY') 
	CONSUMER_SECRET = cfg.get('twitter', 'CONSUMER_SECRET')

	oauth = twitter.oauth.OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
	# Initiate the connection to Twitter REST API
	twitter_api = twitter.Twitter(auth=oauth)



	for x in range( 0, numUpdates ):
		
		phrase = redditGenerate.generatePhrases()
		print( phrase )
		if( not debug ):
			status = twitter_api.statuses.update( status=phrase )
		if( (x+1) != numUpdates ):
			time.sleep( timebetween )
		

