import tweepy as tw
import pandas as pd
import csv

consumer_key = "UDdkyB8Ic9cS6LnANJE04zUUy"
consumer_secret = "XL1HdDN09pYa53znWlKVx7CR5C2nIsgv3Z0LITYY9Xuqs14YBZ"
access_token = "1324310603318677504-l7zTT3OfLsXNyCCOaLw6pV7lOEBsZG"
access_token_secret = "ryvrGpAaflFWJORgAtGC2Q215Qaoxj1ZLCO8yogo8Zu90"

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# To obtain therock tweets
other_user = "realDonaldTrump"
data = []
for status in tw.Cursor(api.user_timeline, screen_name=other_user).items(10):
    data.append(status.text)
print(data)
dataframe = pd.DataFrame(data)
dataframe.to_csv("politici_trump.csv", index=False, header=False)


replies = []
for full_tweets in tw.Cursor(api.user_timeline,screen_name=other_user,timeout=999999).items(10):
    for tweet in tw.Cursor(api.search,q='to:'+other_user,result_type='recent',timeout=999999).items(10):
        if hasattr(tweet, 'in_reply_to_status_id_str'):
            if tweet.in_reply_to_status_id_str==full_tweets.id_str:
                replies.append(tweet.text)
            print("Tweet :",full_tweets.text)
            for elements in replies:
                print("Replies :", elements)
    comments = pd.DataFrame(replies)
    comments.to_csv("comments.csv", index=False, header=False)
