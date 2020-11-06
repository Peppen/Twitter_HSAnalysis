import tweepy as tw

consumer_key = "0aJnar4c0EEjpG4JXwI1YVtW4"
consumer_secret = "VtotsX0e4CN0igfQwAq9lKzeJWY67OY2KcJCFa0To9d0l6WgTR"
access_token = "1324015425546522631-Q5qycHrCIxkmNkMmYMeXWxpbYkttzf"
access_token_secret = "gSqpHs5LrGgobTLlCbAS9CHAMDWJbHqtzm2Q8djNlT3Us"

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# To obtain therock tweets
other_user = "therock"
i=0
for status in tw.Cursor(api.user_timeline, screen_name=other_user).items(10):
    i+=1
    print(i,status.text)

# Search for query
query = "#python"
z=0
for status in tw.Cursor(api.search, q=query).items(50):
    z+=1
    print(z, status.text, status.author.screen_name)