import configparser
import praw
import json
import os
import sys


import utilities

cfg = configparser.ConfigParser()
cfg.read('config.ini')

CLIENT_ID = cfg.get('reddit', 'client_id') 
CLIENT_SECRET = cfg.get('reddit', 'client_secret')
USER_AGENT = cfg.get('reddit', 'user_agent') 

def praw_init():

	print( "Initializing PRAW connection" )
	reddit = praw.Reddit(client_id=CLIENT_ID,
	                     client_secret=CLIENT_SECRET,
	                     user_agent=USER_AGENT
	                     )

	reddit.config.log_requests = 1
	reddit.config.store_json_result = True

	print(reddit.read_only)
	return reddit

def getComments( comment_type ):

	reddit = praw_init()
	comments_json = []

	if( comment_type == 'hot' ):
		comments = reddit.redditor('thingscouldbeworse').comments.hot(limit=None)
	elif( comment_type == 'controversial' ):
		comments = reddit.redditor('thingscouldbeworse').comments.controversial(limit=None)
	elif( comment_type == 'top' ):
		comments = reddit.redditor('thingscouldbeworse').comments.top(limit=None)
	elif( comment_type == 'new' ):
		comments = reddit.redditor('thingscouldbeworse').comments.new(limit=None)

	for comment in comments:
		if( comment.body is not None and comment.id is not None):
			comment_json = { 'id' : comment.id, 'body' : comment.body }
			comments_json.append( comment_json )

	return comments_json

def writeJson( comments_json ):

	with open( os.getcwd() + '/redditComments/' + 'redditDB.json', 'w' ) as DB_file:
		DB_file.write( json.dumps(comments_json, indent=2) )

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

	new_new = getComments( 'new' )
	comments_list = []
	comments_list.append( new_new )

	consolidated = consolidate( comments_list )

	return consolidated

def getAll():

	retrieved_comments = []

	new_hot = getComments( 'hot' )
	new_top = getComments( 'top' )
	new_con = getComments( 'controversial' )
	new_new = getComments( 'new' )

	retrieved_comments.append( new_hot )
	retrieved_comments.append( new_top )
	retrieved_comments.append( new_con )
	retrieved_comments.append( new_new )

	consolidated = consolidate( retrieved_comments )

	return consolidated