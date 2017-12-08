import json

#def get_tweet_type(x):

with open('test.json') as json_data:
    d = json.load(json_data)
    print (json.dumps(d, indent=4))
