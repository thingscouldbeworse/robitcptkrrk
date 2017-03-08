import configparser
import twitter
import json
import redditGenerate
import time
import re

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

def goGetEm( tweetText, debug=False ):

	twitter_api = tweetsRetrieve.connection_init()


	ats = re.findall( '[\@]\w+', tweetText )
	for at in ats:
		if( at.lower() != "@RobitCptKrrk".lower() ):

			characters = at + " "
			num_characters = 140 - len(characters)
			phrase = redditGenerate.generatePhrases( numCharacters=num_characters )
			phrase = characters + phrase

			if( not debug ):
				status = twitter_api.statuses.update( status=phrase )
			else:
				print( phrase )

def checkMentions():

	new_mentions = tweetsRetrieve.getMentions()

	old_mentions = tweetsRetrieve.getDatabase( 'mentions' )

	found = 0
	for new_mention in new_mentions:
		if new_mention not in old_mentions:
			print( "new mention: " + new_mention['text'] )
			
			if( new_mention['screen_name'] == 'CptKrrk' and "go get 'em" in new_mention['text'] ):
				goGetEm( new_mention['text'] )
			else:
				postReply( new_mention['screen_name'], new_mention['id'] )
			found = found + 1


	consolidated = tweetsRetrieve.consolidate( [new_mentions], 'mentions', verbose=False )
	tweetsRetrieve.storeItems( consolidated, 'mentions' )
