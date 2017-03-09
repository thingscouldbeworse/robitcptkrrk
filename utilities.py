import json
import os
import datetime
import pickle

# just straight appends content to the logfile
def log_append( content ):

	timestamp = ('Timestamp: {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()))
	with open("logfile.log","a+") as logfile:
		logfile.write( timestamp + "\n" )
		logfile.write( json.dumps(content, indent=2) )
		logfile.write( "\n" )

