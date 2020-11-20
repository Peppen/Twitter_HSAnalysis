import csv
import tweepy
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import numpy as np
import re
import logging
import time

analyser = SentimentIntensityAnalyzer()
def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))


consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Use this function to do some tests
# Calculate score for each tweet and append it to the csv (to complete)
def calculate_vader_score(username, category):
    text_for_vader = []
    df = pd.read_csv(category + "_" + username + "_all.csv")
    #Reply cleaning
    for i, row in df.iterrows():
        row["Reply"] = re.sub(r"https?://[A-Za-z0-9./]*", '', row["Reply"])
        row["Reply"] = re.sub(r"@[\w]*",'', row["Reply"])
        row["Reply"] = re.sub(r"RT @[\w]*:",'',row["Reply"])
        row["Reply"] = re.sub(r"RT :",'',row["Reply"])
        row["Reply"] = row["Reply"].replace("RT",'')
        if row["Reply"][0] == 'b':
            row["Reply"] = row["Reply"][1:]
        df.loc[i,"Reply"] = row["Reply"]

        #print(len(df.loc[i,"Reply"]))
        print(df.loc[i,"Reply"][0:3])
        df = df[df.Reply != "' '"]
        df = df[df.Reply != "'  '"]

    df.to_csv("test_all.csv",sep=',')

    #for i,row in text_for_vader:

    #sentiment_analyzer_scores(x)


def csv_from_tweets(username, category):
    #CSV HEADER
    tweet = [["ID","Username", "Data", "Tweet", "Reply"]]
    i=0
    #non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    #iterate through tweets
    for full_tweets in tweepy.Cursor(api.user_timeline, screen_name=username, timeout=999999).items(2):
        print(full_tweets.id_str)
        i+=1
        #iterate through replies
        for full_replies in tweepy.Cursor(api.search, q='to:' + username, since_id = full_tweets.id , timeout=999999).items(10):
            #print("contareply")
            #print(full_tweets.id_str)
            #print("id reply"+str(full_replies.in_reply_to_status_id_str))
            if hasattr(full_replies, 'in_reply_to_status_id_str'):
                if full_replies.in_reply_to_status_id_str == full_tweets.id_str:
                    #create an array list composed by the tweet and its replies
                    tweet.append([i,username, full_tweets.created_at, full_tweets.text.encode("ascii", "ignore"), full_replies.text.encode("ascii","ignore")])


    outfile = category + "_" + username + "_all.csv"
    print("writing to " + outfile)
    with open(outfile, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(tweet)


if __name__ == '__main__':
    # Fornisco l'username e categoria
    username = "realDonaldTrump"
    category = "politici"
    csv_from_tweets(username, category)
    calculate_vader_score(username, category)

	# users = ['therock','realDonaldTrump']
	# for user in users:
		# get_tweets(user,categoria)
