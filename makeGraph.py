import csv
import os
import pandas as pd
import matplotlib.pyplot as plt


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
            plt.ylabel('Rate')
            plt.xlabel('Iterations')
            plt.title("Hate Offensive and Neither Rate of " + f.title())
            plt.plot(positive_rate)
            plt.plot(negative_rate)
            plt.plot(neutral_rate)
            plt.show()


def makeHateOffensiveGraph(category):
    os.chdir("C:\\Users\\peppe\\PycharmProjects\\Twitter_HSAnalysis\\" + category)
    for f in os.listdir():
        if f.endswith("_average.csv"):
            df = pd.read_csv(f)
            hate_rate = df["Hate Rate"]
            offensive_rate = df["Offensive rate"]
            neither_rate = df["Neither rate"]
            plt.title("Hate Offensive and Neither Rate of " + f.title())
            plt.ylabel('Rate')
            plt.xlabel('Iterations')
            plt.plot(hate_rate)
            plt.plot(offensive_rate)
            plt.plot(neither_rate)
            plt.show()
