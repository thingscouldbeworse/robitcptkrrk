import configparser
import twitter
import json
import redditGenerate
import time

import tweetsRetrieve

def postUpdate( numUpdates=1, timebetween=0, debug=False ):

	twitter_api = tweetsRetrieve.connection_init()

	for x in range( 0, numUpdates ):
		
		phrase = redditGenerate.generatePhrases()
		print( phrase )
		
		if( not debug ):
			status = twitter_api.statuses.update( status=phrase )
			print( status['text'] )

		if( (x+1) != numUpdates ):
			time.sleep( timebetween )

def postReply( screenName, replyID, debug=False ):

	twitter_api = tweetsRetrieve.connection_init()

	characters = "@" + screenName + " "
	num_characters = 140 - len(characters)
	phrase = redditGenerate.generatePhrases( numCharacters=num_characters )
	phrase = characters + phrase

	if( not debug ):
		status = twitter_api.statuses.update( status=phrase, in_reply_to_status_id=replyID )
	else:
		print( phrase )


