import configparser
import praw
import json

cfg = configparser.ConfigParser()
cfg.read('config.ini')

CLIENT_ID = cfg.get('reddit', 'client_id') 
CLIENT_SECRET = cfg.get('reddit', 'client_secret')
USER_AGENT = cfg.get('reddit', 'CONSUMER_KEY') 

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT
                     )

reddit.config.log_requests = 1
reddit.config.store_json_result = True

print(reddit.read_only)

comments_json = []
		


for comment in reddit.redditor('thingscouldbeworse').comments.new(limit=None):
	comment_json = { 'id' : comment.id, 'body' : comment.body }
	comments_json.append( comment_json )

with open( 'redditDB.json', 'w' ) as DB_file:
	DB_file.write( json.dumps(comments_json) )