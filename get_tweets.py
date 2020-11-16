import csv
import tweepy as tw
import pandas as pd
import vaderSentiment

#Credenziali Twitter API

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

#Function to download latest tweets of a user and create a csv
def get_tweets(username, category):

	auth = tw.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tw.API(auth)

	#Number of tweets to download
	number_of_tweets = 100

	#get tweets randomly between a number of 1 to 100
	tweets_for_csv = [["Username","Data","Tweet"]]
	for tweet in tw.Cursor(api.user_timeline, screen_name = username).items(number_of_tweets):
        #create array of tweet information: username, date/time, text
		tweets_for_csv.append([username, tweet.created_at, tweet.text.encode("ascii","ignore")])
	print(len(tweets_for_csv))

	#Writing tweet obtained in a csv
	header = ['Username', 'Data', 'Tweet']
	outfile = category+"_"+username+".csv"
	print("writing to " + outfile)
	#Adding tweets
	with open(outfile, 'w', newline='') as file:
		writer = csv.writer(file,delimiter = ',')
		writer.writerows(tweets_for_csv)
		print("lo faccio")

	replies = []
	for full_tweets in tw.Cursor(api.user_timeline, screen_name=username, timeout=999999).items(2):
		replies.append([username, full_tweets.id_str, full_tweets.created_at, full_tweets.text.encode("utf-8")])
		print("Full_tweet: " + full_tweets.text)
		for tweet in tw.Cursor(api.search, q='to:'+username, result_type='recent', timeout=999999).items(1000):
			if hasattr(tweet, 'in_reply_to_status_id_str'):
				if tweet.in_reply_to_status_id_str == full_tweets.id_str:
					replies.append([tweet.text.encode("utf-8")])
					print("Tweet :", tweet.text)
	for elements in replies:
		print("Replies :", elements)
	nome_categoria = "actors"
	outfile = nome_categoria + "_" + username + ".csv"
	print("writing to " + outfile)
	with open(outfile, 'w+') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerows(replies)

#Calculate score for each tweet and append it to the csv (to complete)
def calculate_vader_score(username, category):
	text_for_vader = []
	df = pd.read_csv(category+"_"+username+".csv")
	for i,row in df.iterrows():
		text_for_vader.append(row["Tweet"].replace('RT',''))