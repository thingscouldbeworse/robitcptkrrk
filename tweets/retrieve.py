import markovify
import configparser
import twitter

cfg = configparser.ConfigParser()
cfg.read('config.ini')

ACCESS_TOKEN = cfg.get('twitter', 'ACCESS_TOKEN') 
ACCESS_SECRET = cfg.get('twitter', 'ACCESS_SECRET')
CONSUMER_KEY = cfg.get('twitter', 'CONSUMER_KEY') 
CONSUMER_SECRET = cfg.get('twitter', 'CONSUMER_SECRET')

oauth = twitter.oauth.OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)
# Initiate the connection to Twitter REST API
twitter_api = twitter.Twitter(auth=oauth)

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

end = 0
start = 1

tweetDB = open( 'tweetDB', 'w' )
for tweet in all_tweets:
	tweetDB.write( str(tweet['id']) + ', "' + tweet['text'] + '"\n' )
