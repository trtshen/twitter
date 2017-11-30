'''Tweet Streaming API consumer'''
import twitter, csv, json

# == OAuth Authentication ==
consumer_key="HUcXih4iRVgoyV13IqxRlS5BU"
consumer_secret="QUcm0AWx75ajw5Ewqepu4b43pXw1QdswpTrCl9VPcvodIPx2jZ"
access_token="113197842-iicH3rBNj41yzehS4ke3Ft5BiZW3vcelQj40BVnl"
access_token_secret="ijBDkBNxmkVy0JtLsyVaVZOzzIk3KVaD7uX9XB7Tx8x8l"


auth = twitter.oauth.OAuth(access_token, access_token_secret, consumer_key, consumer_secret)
twitter_api = twitter.Twitter(auth=auth)

csvfile = open('starwars.csv', 'w')
csvwriter = csv.writer(csvfile,delimiter ='|')

# csvwriter.writerow(['created_at',
#                     'user-screen_name',
#                     'text',
#                     'coordinates lng',
#                     'coordinates lat',
#                     'place',
#                     'user-location',
#                     'user-geo_enabled',
#                     'user-lang',
#                     'user-time_zone',
#                     'user-statuses_count',
#                     'user-followers_count',
#                     'user-friends_count',
#                     'user-created_at',
#                     'user-source'])

q = "starwars"

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
    # print json.dumps(tweet)
    try:
        if tweet['truncated']:
            tweet_text = tweet['extended_tweet']['full_text']
        else:
            tweet_text = tweet['text']
        csvwriter.writerow([tweet['created_at'],
                            clean(tweet['user']['screen_name']),
                            clean(tweet_text),
                            getLng(tweet['coordinates']),
                            getLat(tweet['coordinates']),
                            getVal(tweet['user']['location']),
                            tweet['user']['created_at'],
                            tweet['user']['followers_count'],
                            tweet['user']['friends_count'],
                            tweet['user']['statuses_count'],
                            clean(tweet['source']),
                            clean(tweet['user']['location']),
                            tweet['user']['geo_enabled'],
                            tweet['user']['lang'],
                            clean(tweet['user']['time_zone'])
                            ])
        print tweet_text
    except Exception, err:
        print err
        pass


print "done"
