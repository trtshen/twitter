import json

# To identify the tweet type
def get_tweet_type(tweet_obj):
	# Set default value as normal
	# Anything that does not fullfill the if else condition,
	# will get the results as normal
	result = 'normal'

	# if retweeted_status exist in the json object,
	# this tweet belongs to retweet
	if 'retweeted_status' in tweet_obj:
		result = 'retweet'
	# if quoted_status exist in the json object,
	# this tweet belongs to quote_tweet
	elif 'quoted_status' in tweet_obj:
		result = 'quote_tweet'

	return result

# To get the correct truncated value based on tweet_type
def get_tweet_status(x):
	# tweet_type value is get based on the get_tweet_type function
	tweet_type = x['tweet_type']

	# Put a default value in tweet status
	# So that if all does not meet the if-else condition
	# We can check on the particular record
	# As it does not fullfill our requirement
	tweet_status = None

	# if tweet_type is normal,
	# system will only check the outer level of the truncated status
	if tweet_type =='normal':
		tweet_status = x['truncated']

	# if tweet_type is retweet,
	# system will get the truncated value from retweeted_status
	elif tweet_type =='retweet':
		tweet_status = x['retweeted_status']['truncated']

	# if tweet_type is quote_tweet,
	# system will get the truncated value from quoted status
	elif tweet_type=='quote_tweet':
		tweet_status = x['quoted_status']['truncated']

	return tweet_status

# To get the correct tweet text, based on twitter type and twitter status
def get_tweet_text(x):

	# Get the value of tweet_type 
	# Value : normal, retweet, quote_tweet
	tweet_type = x['tweet_type']

	# Get the value of tweet_status
	# Value : True, False
	tweet_status = x['tweet_status_truncated']

	# Set tweet_msg as None by default,
	# To check if any message does not fullfill the if else condition
	tweet_msg = None

	# Condition Checking
	# 
	# if tweet_type message is normal
	if tweet_type == 'normal':

		# if the tweet_status is True
		# Mean text been truncated
		# hence system should get the full text from extended_tweet
		if tweet_status:
			tweet_msg = x['extended_tweet']['full_text']

		# Else = Truncated status is false
		# System can take back the original text
		else:
			tweet_msg = x['text']

	# if the tweet_typs is retweet
	elif tweet_type =='retweet':

		# if the tweet_status is True
		# Mean text been truncated
		# System get the full text from retweeted_status -> extended_tweet
		if tweet_status:
			tweet_msg = x['retweeted_status']['extended_tweet']['full_text']

		# Else , full text can be retrieved in retweeted_status
		else:
			tweet_msg = x['retweeted_status']['text']


	# if the tweet_type is quote tweet
	elif tweet_type=='quote_tweet':
		# if the tweet status is True
		# retrieve full text from quoted status -> extended_tweet
		if tweet_status:
			tweet_msg = x['quoted_status']['extended_tweet']['full_text']

		# retrieve from quoted_Status
		else:
			tweet_msg = x['quoted_status']['text']

	return tweet_msg


# main application
with open('result.json') as json_data:
    raw_json = json.load(json_data)
    
new_dict = []
for each_rec in raw_json:

	# To Identify what is the tweeter message type
	each_rec['tweet_type'] = get_tweet_type(each_rec)

	# Once get the message type, to check the tweet status
	# Whether it has been truncated or not
	each_rec['tweet_status_truncated'] = get_tweet_status(each_rec)
	
	# Check tweet type and tweet status
	# Determine which field to get
	each_rec['tweet_text'] = get_tweet_text(each_rec)


#new_dict.append(each_rec)

#print (json.dumps(new_dict,indent=4))



