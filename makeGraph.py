import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def calculateAvarage(category):
    os.chdir("C:\\Users\\peppe\\PycharmProjects\\Twitter_HSAnalysis\\" + category)
    for f in os.listdir():
        if f.endswith("_rates.csv"):
            df = pd.read_csv(f)
            pos_sum = 0
            neg_sum = 0
            neut_sum = 0
            hatespeech_sum = 0
            offensive_sum = 0
            neither_sum = 0
            rates = []

            for i, row in df.iterrows():
                username = row["Username"]
                pos_sum += row["Positive Rate"]
                neg_sum += row["Negative Rate"]
                neut_sum += row["Neutral Rate"]
                hatespeech_sum += row["Hate Rate"]
                offensive_sum += row["Offensive rate"]
                neither_sum += row["Neither rate"]

            pos_sum = str(round((pos_sum / 5), 2))
            neg_sum = str(round((neg_sum / 5), 2))
            neut_sum = str(round((neut_sum / 5), 2))
            hatespeech_sum = str(round((hatespeech_sum / 5), 2))
            offensive_sum = str(round((offensive_sum / 5), 2))
            neither_sum = str(round((neither_sum / 5), 2))

            rateFile = "./" + category + "_average.csv"

            if os.path.isfile(rateFile):
                rates.append(
                    [username, category, pos_sum, neg_sum, neut_sum, hatespeech_sum, offensive_sum, neither_sum])
                with open(rateFile, 'a', newline='') as file:
                    writer = csv.writer(file, delimiter=',')
                    writer.writerows(rates)
            else:
                rates=[["Username", "Category", "Positive Rate", "Negative Rate", "Neutral Rate", "Hate Rate","Offensive rate", "Neither rate"]]
                rates.append([username, category, pos_sum, neg_sum, neut_sum, hatespeech_sum, offensive_sum, neither_sum])
                with open(rateFile, 'w', newline='') as file:
                    writer = csv.writer(file, delimiter=',')
                    writer.writerows(rates)


def makePositiveNegativeRate(category):
    os.chdir("C:\\Users\\peppe\\PycharmProjects\\Twitter_HSAnalysis\\" + category)
    for f in os.listdir():
        if f.endswith("_average.csv"):
            df = pd.read_csv(f)
            positive_rate = df["Positive Rate"]
            negative_rate = df["Negative Rate"]
            neutral_rate = df["Neutral Rate"]
            plt.title("Results of " + category)
            rate = ["Positive Rate", "Negative Rate", "Neutral Rate"]
            positives = 0
            negatives = 0
            neutrals = 0
            for positive in positive_rate:
                positives += positive
            positives = positives/len(positive_rate)
            for negative in negative_rate:
                negatives += negative
            negatives = negatives/len(negative_rate)
            for neutral in neutral_rate:
                neutrals += neutral
            neutrals = neutrals / len(neutral_rate)
            results = [positives, negatives, neutrals]
            plt.yticks(results)
            plt.bar(rate, results)
            plt.show()


def makeHateOffensiveGraph(category):
    os.chdir("C:\\Users\\peppe\\PycharmProjects\\Twitter_HSAnalysis\\" + category)
    for f in os.listdir():
        if f.endswith("_average.csv"):
            df = pd.read_csv(f)
            hate_rate = df["Hate Rate"]
            offensive_rate = df["Offensive rate"]
            neither_rate = df["Neither rate"]
            plt.title("Results of " + category)
            rate = ["Hate Rate", "Offensive Rate", "Neither Rate"]
            hates = 0
            offensives = 0
            neithers = 0
            for hate in hate_rate:
                hates += hate
            hates = hates/len(hate_rate)
            for offensive in offensive_rate:
                offensives += offensive
            offensives = offensives/len(offensive_rate)
            for neither in neither_rate:
                neithers += neither
            neithers = neithers/len(neither_rate)
            results = [hates, offensives, neithers]
            plt.yticks(results)
            plt.bar(rate, results)
            plt.show()
