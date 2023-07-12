from __future__ import absolute_import, print_function
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re
import csv
import json
import time

ckey = '03FBLHYRb6wccc3NtCAgcoIcT'
csecret ='u1pc6fykISbggyWpRXfPkVxqTxE4Xo5AKTcTnKG1FLQdCiMNlm'
atoken = '128811050-Xxt18nrSxY1Ptq7tNgZtxM1XghLQSz3sFb7cI7Gt'
asecret = 'kUBmjHDsSg7WSsTBg4C8QCdCGsAT0F1zufcs2jyb9xdnj'


class listener(StreamListener):
    def on_data(self,data):
        try:
            tweet=  json.loads(data)
            print(tweet)
            tweet = tweet['text']
            print (tweet)
            savetweet='"'+tweet+'"'; 
            saveFile = open('raw_data.csv','a')
            saveFile.write(savetweet)
            saveFile.write('\n')
            saveFile.close()
            return False
        except BaseException as  e:
             print('failed ondata.',str(e))
             time.sleep(5)
    def on_error(self, status):
        print(status)

def mainf(inp):
    if inp is not None:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=[inp])
