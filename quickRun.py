import sys
import os

sys.path.append( os.getcwd() + '/redditComments/' )

import redditRetrieve
import redditGenerate

consolidated = redditRetrieve.getAll()

redditRetrieve.writeJson( consolidated )
print( redditGenerate.generatePhrases() )
