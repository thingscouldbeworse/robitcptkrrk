import configparser
import praw
import json
import os

cfg = configparser.ConfigParser()
cfg.read('config.ini')

CLIENT_ID = cfg.get('reddit', 'client_id') 
CLIENT_SECRET = cfg.get('reddit', 'client_secret')
USER_AGENT = cfg.get('reddit', 'user_agent') 

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT
                     )

reddit.config.log_requests = 1
reddit.config.store_json_result = True

print(reddit.read_only)


def getNew():

	comments_json = []

	for comment in reddit.redditor('thingscouldbeworse').comments.new(limit=None):
		comment_json = { 'id' : comment.id, 'body' : comment.body }
		comments_json.append( comment_json )

	return comments_json

def getTop():

	comments_json = []

	for comment in reddit.redditor('thingscouldbeworse').comments.top(limit=None):
		comment_json = { 'id' : comment.id, 'body' : comment.body }
		comments_json.append( comment_json )

	return comments_json

def getControversial():

	comments_json = []

	for comment in reddit.redditor('thingscouldbeworse').comments.controversial(limit=None):
		comment_json = { 'id' : comment.id, 'body' : comment.body }
		comments_json.append( comment_json )

	return comments_json

def getHot():

	comments_json = []

	for comment in reddit.redditor('thingscouldbeworse').comments.top(limit=None):
		comment_json = { 'id' : comment.id, 'body' : comment.body }
		comments_json.append( comment_json )

	return comments_json

def writeJson( comments_json ):

	with open( os.getcwd() + '/redditComments/' + 'redditDB.json', 'w' ) as DB_file:
		DB_file.write( json.dumps(comments_json) )

def consolidate( comment_list ):

	with open( os.getcwd() + '/redditComments/' + 'redditDB.json' ) as json_data:
		all_comments = json.load(json_data)
		json_data.close()

	print( str(len( all_comments )) + " comments in DB to start" )

	for comments_json in comment_list:
		for comment in comments_json:
			if comment not in all_comments:
			
				all_comments.append( comment )
			

	print( str(len( all_comments )) + " comments now in DB" )

	return all_comments

def getRecentNew():

	new_new = getNew()

	consolidated = consolidate( new_new )

	return consolidated

def getAll():

	retrieved_comments = []

	new_hot = getHot()
	new_top = getTop()
	new_con = getControversial()
	new_new = getNew()

	retrieved_comments.append( new_hot )
	retrieved_comments.append( new_top )
	retrieved_comments.append( new_con )
	retrieved_comments.append( new_new )

	consolidated = consolidate( retrieved_comments )

	return consolidated