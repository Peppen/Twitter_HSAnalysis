import tweepy as tw
import pandas as pd
import csv

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# To obtain therock tweets
other_user = "therock"
i=0
dict = {}
for status in tw.Cursor(api.user_timeline, screen_name=other_user).items(10):
    i+=1
    data = {"Status" : status.text}
    df = pd.DataFrame.from_dict(data, orient='index')
    df.to_csv('dataFrame.csv')
    print(df)

replies=[]
for full_tweets in tw.Cursor(api.user_timeline,screen_name=other_user,timeout=999999).items(10):
  for tweet in tw.Cursor(api.search,q='to:'+other_user,result_type='recent',timeout=999999).items(10):
    if hasattr(tweet, 'in_reply_to_status_id_str'):
      if (tweet.in_reply_to_status_id_str==full_tweets.id_str):
        replies.append(tweet.text)
  print("Tweet :",full_tweets.text)
  for elements in replies:
       print("Replies :",elements)
  replies.clear()
