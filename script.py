import csv
import tweepy
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyser = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))


consumer_key = "0aJnar4c0EEjpG4JXwI1YVtW4"
consumer_secret = "VtotsX0e4CN0igfQwAq9lKzeJWY67OY2KcJCFa0To9d0l6WgTR"
access_token = "1324015425546522631-kcL1Ama0t8MvM425oefeXyginFI51t"
access_token_secret = "5w5EBpiKR54ySybSLK8XlRx2IcCXaN2eleS4G3VhjfLSG"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def get_tweets(username, category):
    # Number of tweets to download
    number_of_tweets = 100
    # get tweets randomly between a number of 1 to 100
    tweets_for_csv = [["Username", "Data", "Tweet"]]
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=username).items(number_of_tweets):
        # create array of tweet information: username, date/time, text
        tweets_for_csv.append([username, tweet.created_at, tweet.text.encode("ascii", "ignore")])
    print(len(tweets_for_csv))

    # Writing tweet obtained in a csv
    header = ['Username', 'Data', 'Tweet']
    outfile = category + "_" + username + "_tweets.csv"
    print("writing to " + outfile)
    # Adding tweets
    with open(outfile, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(tweets_for_csv)


# Use this function to do some tests
# Calculate score for each tweet and append it to the csv (to complete)
def calculate_vader_score(username, category):
    text_for_vader = []
    df = pd.read_csv(category + "_" + username + "_tweets.csv")
    for i, row in df.iterrows():
        text_for_vader.append(row["Tweet"].replace('RT', ''))
    for x in text_for_vader:
        if x[0] == 'b':
            x = x[1:]

        # Your code here
        print(x)
        sentiment_analyzer_scores(x)


def get_comments_from_tweets(username, category):
    replies = []
    for full_tweets in tweepy.Cursor(api.user_timeline, screen_name=username, timeout=999999).items(2):
        replies.append([username, full_tweets.id_str, full_tweets.created_at, full_tweets.text.encode("ascii", "ignore")])
        print("Full_tweet: " + full_tweets.text)
        for tweet in tweepy.Cursor(api.search, q='to:' + username, result_type='recent', timeout=999999).items(10):
            if hasattr(tweet, 'in_reply_to_status_id_str'):
            # if tweet.in_reply_to_status_id_str == full_tweets.id_str:
                replies.append([tweet.text.encode("ascii", "ignore")])
                print("Tweet :", tweet.text)
    outfile = category + "_" + username + "_comments.csv"
    print("writing to " + outfile)
    with open(outfile, 'w+') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(replies)


if __name__ == '__main__':
    # Fornisco l'username e categoria
    username = "realDonaldTrump"
    category = "politici"
    get_tweets(username, category)
    calculate_vader_score(username, category)
    get_comments_from_tweets(username, category)

	# users = ['therock','realDonaldTrump']
	# for user in users:
		# get_tweets(user,categoria)
