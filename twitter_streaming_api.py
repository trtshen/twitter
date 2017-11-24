import twitter, json, sys, csv

# == OAuth Authentication ==
consumer_key="GXbUDGfeYjHGuURCvmBTpbBqS"
consumer_secret="VFDJZaO0fL1VXcA7zQbPahBqokyqyUOzARaL3l0SBeN0Nif3en"
access_token="113197842-xRrss0ZJbyiUq5eV4fyd0Mf0bRHUHvoCTAAtX2SE"
access_token_secret="NagevuIxsC2r3T33e4C5Yof6kPWxMKDbDtNlK50mCrmil"

auth = twitter.oauth.OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
twitter_api = twitter.Twitter(auth=auth)

csvfile = open('kltu_data.csv', 'w')
csvwriter = csv.writer(csvfile)
csvwriter.writerow([['created_at'],
					['screen_name'],
					['text'],
					['created_at'],
					['followers_count'],
					['friends_count'],
					['statuses_count'],
					['source'],
					['location'],
					['geo_enabled'],
					['lang'],
					['time_zone'],
					['retweet_count']
					])


q = "kltu"

# small function encapsuate the encodes and protect replace nulls with empty values
def clean(val):
	clean = ""
	if val:
		clean = val.encode('utf-8')
	return clean


print 'Filtering the public timeline for keyword="%s"' % (q)
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
stream = twitter_stream.statuses.filter(track=q)

for tweet in stream:
 	# print json.dumps(tweet)
    try:
        csvwriter.writerow([tweet['created_at'],
                            clean(tweet['user']['screen_name']),
                            clean(tweet['text']),
                            tweet['user']['created_at'],
                            tweet['user']['followers_count'],
                            tweet['user']['friends_count'],
                            tweet['user']['statuses_count'],
                            clean(tweet['source']),
                            clean(tweet['user']['location']),
                            tweet['user']['geo_enabled'],
                            tweet['user']['lang'],
                            clean(tweet['user']['time_zone']),
                            tweet['retweet_count']
                            ])

        print tweet['user']['screen_name'].encode('utf-8'), tweet['text'].encode('utf-8')
    except Exception as e:
        print e.message
        # just print the error and keep going! we don't care if we lose a few tweets due to errors
        # in a production version of this code we would write the errors into seperate file
        pass


print "done"
