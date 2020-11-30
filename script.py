from twarc import Twarc
import csv
import re
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from hatesonar.api import Sonar
import os.path
import makeGraph as gr

t = Twarc("", "", "", "")
#rateFile = "rates.csv"

# Function that create the .csv of replies
def get_replies(username, category):
    i = 0
    replies = [["Username", "Data", "Reply"]]
    # Select randomly a tweet from the selected user (username)
    for tweet in t.search(username, max_pages=1, result_type='recent'):
        # Get replies to that tweet
        for reply in t.replies(tweet):
            replies.append([username, reply["created_at"], reply["full_text"].encode("ascii", "ignore")])
            if i == 10:
                break
            i += 1

    outfile = "./" + category + "/" + username + "_replies.csv"
    print("writing to " + outfile)
    with open(outfile, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerows(replies)


# Function that clean replies from everything that is not meaningful to vader
def csv_cleaning(username, category):
    df = pd.read_csv("./" + category + "/" + username + "_replies.csv")

    space_pattern = '\s+'

    # Reply cleaning
    for i, row in df.iterrows():
        row["Reply"] = re.sub(r"https?://[A-Za-z0-9./]*", '', row["Reply"])
        row["Reply"] = re.sub(r"@[\w]*", '', row["Reply"])
        row["Reply"] = re.sub(r"RT @[\w]*:", '', row["Reply"])
        row["Reply"] = re.sub(r"RT :", '', row["Reply"])
        row["Reply"] = re.sub(space_pattern, ' ', row["Reply"])
        row["Reply"] = row["Reply"].replace("RT", '')

        # Cleaning quotes from row Reply
        row["Reply"] = row["Reply"].replace("  ", '')
        row["Reply"] = row["Reply"].replace("   ", '')
        row["Reply"] = row["Reply"].replace("    ", '')

        # Deleting 'b' char at the beginning of the text
        if row["Reply"][0] == 'b':
            row["Reply"] = row["Reply"][1:]

        # Update the dataframe with the new rows
        df.loc[i, "Reply"] = row["Reply"].lower()

        # Deleting rows that have no replies
        df = df[df.Reply != "' '"]
        df = df[df.Reply != "'  '"]
        df = df[df.Reply != "'   '"]

    df.to_csv("./" + category + "/" + username + "_replies.csv", sep=',', index=False)


# Function to calculate vader score and add it to the .csv
def calculate_vader_score(username, category):
    analyser = SentimentIntensityAnalyzer()
    vader_score = []
    df = pd.read_csv("./" + category + "/" + username + "_replies.csv")

    # Calculating vader score for each reply
    for i in range(df['Reply'].shape[0]):
        # print(analyser.polarity_scores(sentiments_pd['text'][i]))
        pos = analyser.polarity_scores(df['Reply'][i])["pos"]
        neu = analyser.polarity_scores(df['Reply'][i])["neu"]
        neg = analyser.polarity_scores(df['Reply'][i])["neg"]

        vader_score.append({"Positive": round(pos, 2),
                            "Negative": round(neg, 2),
                            "Neutral": round(neu, 2)
                            })

    # Adding vader scores as columns to .csv file
    sentiments_score = pd.DataFrame.from_dict(vader_score)
    df = df.join(sentiments_score)

    # Dropping rows that aren't calculated well by vader
    for i, row in df.iterrows():
        if row["Neutral"] == 1.0:
            df.drop(i, inplace=True)
    # Adding an index column
    id = range(1, len(df) + 1)
    df.insert(0, "ID", id)

    df.to_csv("./" + category + "/" + username + "_replies.csv", sep=',', index=False)


# Function to calculate hate speech score and append to the .csv
def calculate_hatespeech_score(username, category):
    sonar = Sonar()
    hatespeech_score = []

    df = pd.read_csv("./" + category + "/" + username + "_replies.csv")
    for i in range(df['Reply'].shape[0]):
        score = sonar.ping(df['Reply'][i])
        hate = round(score["classes"][0]["confidence"],2)
        offensive = round(score["classes"][1]["confidence"],2)
        neither = round(score["classes"][2]["confidence"],2)

        hatespeech_score.append({
            "Hate": hate,
            "Offensive": offensive,
            "Neither": neither
        })

    hate_score = pd.DataFrame.from_dict(hatespeech_score)
    df = df.join(hate_score)

    df.to_csv("./" + category + "/" + username + "_replies.csv", sep=',', index=False)

# Function that creates a .csv file containing for each user the average scores obtained
def create_score_csv(username, category):
    df = pd.read_csv("./"+category+"/"+username+"_replies.csv")
    pos_sum = 0
    neg_sum = 0
    neut_sum = 0
    hatespeech_sum = 0
    offensive_sum = 0
    neither_sum = 0
    rates = []



    for i,row in df.iterrows():
        pos_sum += row["Positive"]
        neg_sum += row["Negative"]
        neut_sum += row["Neutral"]
        hatespeech_sum += row["Hate"]
        offensive_sum += row["Offensive"]
        neither_sum += row["Neither"]

    pos_sum = str(round((pos_sum / len(df.index))*100,2))
    neg_sum = str(round((neg_sum / len(df.index))*100,2))
    neut_sum = str(round((neut_sum / len(df.index))*100,2))
    hatespeech_sum = str(round((hatespeech_sum / len(df.index))*100,2))
    offensive_sum = str(round((offensive_sum / len(df.index))*100,2))
    neither_sum = str(round((neither_sum / len(df.index))*100,2))


    rateFile = "./"+category+"/"+username+"_rates.csv"


    if(os.path.isfile(rateFile)):
        rates.append([username, category, pos_sum, neg_sum, neut_sum, hatespeech_sum, offensive_sum, neither_sum])
        with open(rateFile, 'a', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(rates)
    else:
        rates = [["Username","Category","Positive Rate","Negative Rate","Neutral Rate","Hate Rate","Offensive rate", "Neither rate"]]
        rates.append([username, category, pos_sum, neg_sum, neut_sum, hatespeech_sum, offensive_sum, neither_sum])
        with open(rateFile, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=',')
            writer.writerows(rates)

if __name__ == '__main__':
    # Fornisco l'username e categoria
    username = "MarcusRashford"
    category = "Attori"
    #get_replies(username, category)
    #csv_cleaning(username, category)
    #calculate_vader_score(username, category)
    #calculate_hatespeech_score(username, category)
    #create_score_csv(username, category)
    #gr.userAverage(category)
    #gr.vaderGraph(category)
    gr.sonarGraph(category)
