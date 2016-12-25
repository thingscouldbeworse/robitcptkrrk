import postTweet
import schedule
import time
import random

reset = "2:00"
time1 = "10:30"
time2 = "14:30"
time3 = "18:30"

def job():
	chance = random.randint(1,10)
	if( chance > 2 ):
		postTweet.postUpdate( 1, 0 )

	print( "Die roll says no tweet" )

def dayStart():

	time1 = str( random.randint(9,11) ) + ":" + str( random.randint(0,5) ) + str( random.randint(0,9) )
	time2 = str( random.randint(13,15) ) + ":" + str( random.randint(0,5) ) + str( random.randint(0,9) ) 
	time3 = str( random.randint(17,19) ) + ":" + str( random.randint(0,5) ) + str( random.randint(0,9) )  
	print( "times chosen; " )
	print( time1 )
	print( time2 )
	print( time3 )

schedule.every().day.at(reset).do(dayStart)
schedule.every().day.at(time1).do(job)
schedule.every().day.at(time2).do(job)
schedule.every().day.at(time3).do(job)




while True:
	schedule.run_pending()
	time.sleep(1)