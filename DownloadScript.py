import csv
import tweepy
import pandas as pd
import vaderSentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))

#Credenziali Twitter API

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

#Function to download latest tweets of a user and create a csv
def get_tweets(username, category):

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)

	#Number of tweets to download
	number_of_tweets = 100

	#get tweets randomly between a number of 1 to 100
	tweets_for_csv = [["Username","Data","Tweet"]]
	for tweet in tweepy.Cursor(api.user_timeline, screen_name = username).items(number_of_tweets):
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


# Use this function to do some tests
# Calculate score for each tweet and append it to the csv (to complete)
def calculate_vader_score(username, category):
	text_for_vader = []
	df = pd.read_csv(category + "_" + username + ".csv")
	for i, row in df.iterrows():
		text_for_vader.append(row["Tweet"].replace('RT', ''))
	for x in text_for_vader:
		if(x[0] == 'b'):
			x = x[1:]

#Your code here
		print(x)
		sentiment_analyzer_scores(x)


if __name__ == '__main__':
	#Fornisco l'username e categoria
	nome_utente="realDonaldTrump"
	categoria = "politici"
	get_tweets(nome_utente, categoria)
	calculate_vader_score(nome_utente,categoria)

    #metodo alternativo:
	#scorrere tra più utenti, passo più username così verranno
	#creati tanti csv quanti sono gli utenti

	#users = ['therock','realDonaldTrump']

	#for user in users:
		#get_tweets(user,categoria)

#Estrazione dal CSV unicamente la parte di nostro interesse (contenuto)
