import markovify
import configparser
import json

def generatePhrases( numPhrases=1):

	with open( 'redditDB.json' ) as json_data:
		all_comments = json.load(json_data)
		json_data.close()


	text_chunk = ""
	for comment in all_comments:
		
		text = comment['body']

		if( text[-1] != '.' and text[-1] != '!' and text[-1] != '?' and text[-2:] != '. ' and text[-2:] != '! ' and text[-2:] != '? ' ):

			text_chunk = text_chunk + " " + text + '. '

		else:
			text_chunk = text_chunk + text
				
	#print( text_chunk )
	text_model = markovify.Text( text_chunk, state_size=2 )
	for i in range(numPhrases):
		return( text_model.make_short_sentence(140, tries=100) )