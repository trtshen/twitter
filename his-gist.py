'''Tweet Streaming API consumer'''
import twitter, csv, json, sys

# == OAuth Authentication ==
consumer_key="4e22BP6rGNSmvYeifBlrnESB2"
consumer_secret="jDe6CaQcKfbIcWAy0miHHYQLSatD9lVBZ2JA8z2zQtMU2TEPi8"
access_token="113197842-4OIU8sPnWbQm9tKcEOWJbgirz4n3xwtcFXgTmrGE"
access_token_secret="NQRaoIIyMVasxPGMWGqf6zzkqUb4afVagmjQVRZ5AvJd0"

auth = twitter.oauth.OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
twitter_api = twitter.Twitter(auth=auth)

csvfile = open('brexit.csv', 'w')
csvwriter = csv.writer(csvfile,delimiter ='|')

csvwriter.writerow(['created_at',
                    'user-screen_name',
                    'text',
                    'coordinates lng',
                    'coordinates lat',
                    'user-location',
                    'user-created_at',
                    'user-followers_count',
                    'user-friends_count',
                    'user-statuses_count',
                    'source'
                    'user-location',
                    'user-geo_enable',
                    'user-lang',
                    'user-time_zone',
                    ])

q = "brexit"

# clean up our data so we can write unicode to CSV
def clean(val):
    clean = ""
    if val:
        val = val.replace('|', ' ')
        val = val.replace('\n', ' ')
        val = val.replace('\r', ' ')
        clean = val.encode('utf-8')
    return clean

print 'Filtering the public timeline for keyword="%s"' % (q)
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)
stream = twitter_stream.statuses.filter(track=q)

''' helper functions, clean data, unpack dictionaries '''
def getVal(val):
    clean = ""
    if isinstance(val, bool):
        return val
    if isinstance(val, int):
        return val
    if val:
        clean = val.encode('utf-8')
    return clean

def getLng(val):
    if isinstance(val, dict):
        return val['coordinates'][0]

def getLat(val):
    if isinstance(val, dict):
        return val['coordinates'][1]

def getPlace(val):
    if isinstance(val, dict):
        return val['full_name'].encode('utf-8')

for tweet in stream:
    print json.dumps(tweet)

    # try:
    #     if tweet['truncated']:
    #         tweet_text = tweet['extended_tweet']['full_text']
    #     else:
    #         tweet_text = tweet['text']
    #
    #     csvwriter.writerow([tweet['created_at'],
    #                         clean(tweet['user']['screen_name']),
    #                         clean(tweet_text),
    #                         getLng(tweet['coordinates']),
    #                         getLat(tweet['coordinates']),
    #                         getVal(tweet['user']['location']),
    #                         tweet['user']['created_at'],
    #                         tweet['user']['followers_count'],
    #                         tweet['user']['friends_count'],
    #                         tweet['user']['statuses_count'],
    #                         clean(tweet['source']),
    #                         clean(tweet['user']['location']),
    #                         tweet['user']['geo_enabled'],
    #                         tweet['user']['lang'],
    #                         clean(tweet['user']['time_zone'])
    #                         ])
    #     print tweet_text
    # except Exception, err:
    #     print err
    #     pass


print "done"