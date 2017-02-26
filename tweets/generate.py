import markovify
import configparser
import twitter
import json
import re

with open( 'tweetDB.json' ) as json_data:
	all_tweets = json.load(json_data)
	json_data.close()

text_chunk = ""
for tweet in all_tweets:
#	print( tweet['text'][:3] + "|" )
	if( tweet['text'][:3] != 'RT ' and tweet['text'][:3] != ' RT' ):
		text = re.sub( '\@.*?[ ]', '', tweet['text'] )
		if( text[-1] != '.' and text[-1] != '!' and text[-1] != '?' ):
			text_chunk = text_chunk + " " + text + '.'

print( text_chunk )
