import csv
import re

import pandas as pd
import tweepy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()


def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))


consumer_key = "0aJnar4c0EEjpG4JXwI1YVtW4"
consumer_secret = "VtotsX0e4CN0igfQwAq9lKzeJWY67OY2KcJCFa0To9d0l6WgTR"
access_token = "1324015425546522631-SAGX4LIGqZ8l5kYHGlBWLtISA14HlW"
access_token_secret = "IXcpNppU7JQKYD8XQgIzVhbOldhaXeVo09fiAKsPkHMdQ"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


# Use this function to do some tests
# Calculate score for each tweet and append it to the csv (to complete)
def calculate_vader_score(username, category):
    text_for_vader = []
    df = pd.read_csv(category + "_" + username + "_all.csv")
    # Reply cleaning
    for i, row in df.iterrows():
        row["Reply"] = re.sub(r"https?://[A-Za-z0-9./]*", '', row["Reply"])
        row["Reply"] = re.sub(r"@[\w]*", '', row["Reply"])
        row["Reply"] = re.sub(r"RT @[\w]*:", '', row["Reply"])
        row["Reply"] = re.sub(r"RT :", '', row["Reply"])
        row["Reply"] = row["Reply"].replace("RT", '')
        if row["Reply"][0] == 'b':
            row["Reply"] = row["Reply"][1:]
        df.loc[i, "Reply"] = row["Reply"]

        print(len(df.loc[i, "Reply"]))
        # df.drop(df[i])

    df.to_csv("test_all.csv", sep=',')

    # for i,row in text_for_vader:
    # sentiment_analyzer_scores(x)


def csv_from_tweets(username, category):
    tweet = [["ID", "Username", "Data", "Tweet", "Reply"]]
    i = 0
    for full_tweets in tweepy.Cursor(api.user_timeline, screen_name=username, timeout=999999).items(5):
        i += 1
        for full_replies in tweepy.Cursor(api.search, q='to:' + username, result_type='recent', timeout=999999).items(50):
            if hasattr(full_replies, 'in_reply_to_status_id_str'):
                if full_tweets.id_str == full_replies.in_reply_to_status_id_str:
                    tweet.append([i, username, full_tweets.created_at, full_tweets.text.encode("ascii", "ignore"),full_replies.text.encode("ascii", "ignore")])
                    print(full_replies.text)

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
