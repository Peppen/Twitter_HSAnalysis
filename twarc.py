from twarc import Twarc

t = Twarc("", "", "", "")
for tweet in t.search("ferguson"):
    for tweet2 in t.replies(tweet):
        if tweet2.in_reply_to_status_id_str == tweet.id_str:
            print(tweet2)

