from twarc import Twarc
import csv
import re
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

t = Twarc("", "", "", "")


def get_replies(username, category):
    i = 0

    replies = [["ID", "Username", "Data", "Reply"]]
    # Select randomly a tweet from the selected user
    for tweet in t.search(username, max_pages=1, result_type='recent'):
        # Get replies to that tweet
        for reply in t.replies(tweet):
            i += 1
            replies.append([i, username, reply["created_at"], reply["full_text"].encode("ascii", "ignore")])
            if i == 10:
                break

    outfile = "./" + category + "/" + username + "_replies.csv"
    print("writing to " + outfile)
    with open(outfile, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(replies)


def csv_cleaning(username, category):
    df = pd.read_csv("./"+category+"/"+username+"_replies.csv")
    #Reply cleaning
    for i, row in df.iterrows():
        row["Reply"] = re.sub(r"https?://[A-Za-z0-9./]*", '', row["Reply"])
        row["Reply"] = re.sub(r"@[\w]*", '', row["Reply"])
        row["Reply"] = re.sub(r"RT @[\w]*:", '', row["Reply"])
        row["Reply"] = re.sub(r"RT :", '', row["Reply"])
        row["Reply"] = row["Reply"].replace("RT", '')
        # Cleaning quotes from row Reply
        row["Reply"] = row["Reply"].replace("  ", "")
        row["Reply"] = row["Reply"].replace("   ", "")
        row["Reply"] = row["Reply"].replace("    ", "")
        if row["Reply"][0] == 'b':
            row["Reply"] = row["Reply"][1:]
        if row["Reply"][1] == '  ':
            row["Reply"] = row["Reply"][1:]
        df.loc[i, "Reply"] = row["Reply"]

        # print(len(df.loc[i,"Reply"]))
        print(df.loc[i, "Reply"][0:3])
        df = df[df.Reply != "' '"]
        df = df[df.Reply != "'  '"]
        df = df[df.Reply != "'   '"]

    df.to_csv("./"+category+"/"+username+"_replies.csv",sep=',',index=False)

def calculate_vader_score(username, category):
    analyser = SentimentIntensityAnalyzer()
    vader_score = []
    df = pd.read_csv("./"+category+"/"+username+"_replies.csv")

    # Declare variables for scores
    compound_list = []
    positive_list = []
    negative_list = []
    neutral_list = []
    for i in range(df['Reply'].shape[0]):
        # print(analyser.polarity_scores(sentiments_pd['text'][i]))
        compound = analyser.polarity_scores(df['Reply'][i])["compound"]
        pos = analyser.polarity_scores(df['Reply'][i])["pos"]
        neu = analyser.polarity_scores(df['Reply'][i])["neu"]
        neg = analyser.polarity_scores(df['Reply'][i])["neg"]

        vader_score.append({"Compound": compound,
                            "Positive": pos,
                            "Negative": neg,
                            "Neutral": neu
                            })

    sentiments_score = pd.DataFrame.from_dict(vader_score)
    df = df.join(sentiments_score)
    df.head()
    df.to_csv("./"+category+"/"+username+"_replies.csv",sep=',',index=False)


if __name__ == '__main__':
    # Fornisco l'username e categoria
    username = "realDonaldTrump"
    category = "Politici"
    get_replies(username, category)
    csv_cleaning(username, category)
    calculate_vader_score(username, category)

