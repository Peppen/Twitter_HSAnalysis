import tweepy as tw
import pandas as pd
import csv

consumer_key = "0aJnar4c0EEjpG4JXwI1YVtW4"
consumer_secret = "VtotsX0e4CN0igfQwAq9lKzeJWY67OY2KcJCFa0To9d0l6WgTR"
access_token = "1324015425546522631-27RiZ39mvUggNR1TPMd0mYkVHCCRWC"
access_token_secret = "DcHVq9sakowrxZORAzDQeeFZU9Y7GMQb2XAVbRHpPOuap"

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# To obtain therock tweets
other_user = "therock"
data = []
for status in tw.Cursor(api.user_timeline, screen_name=other_user).items(10):
    data.append(status.text)
print(data)
dataframe = pd.DataFrame(data)
dataframe.to_csv("dataFrame.csv", index=False, header=False)


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