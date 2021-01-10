import csv
import json
import math

import pandas as pd

df = {'canada': 0, 'rain': 0, 'cold': 0, 'hot': 0}
tfidf = {'canada': 0, 'rain': 0, 'cold': 0, 'hot': 0}
log = {'canada': 0, 'rain': 0, 'cold': 0, 'hot': 0}
global data


def loadnews():
    global data
    print("\nLoading news")
    with open('news.json', 'r') as read_file:
        data = json.load(read_file)


def calculatedf():
    print("\nCalculating DF...")
    global data
    for keyword in df:
        for each in data:
            words = each['title'].lower().split() + each['body'].lower().split()
            each['wordcount'] = len(words)
            occurences = words.count(keyword)
            each[keyword] = occurences
            if occurences > 0:
                df[keyword] += 1
    print('\n')
    print(df)


def calculateTFIDF():
    print("\nCalculating TF-IDF...")
    global data
    for i in df:
        if df[i] != 0:
            tfidf[i] = len(data) / df[i]
    print(tfidf)


def calculateLog():
    print("\nCalculating Log10(N/df)...")
    for i in tfidf:
        if tfidf[i] != 0:
            log[i] = round(math.log10(tfidf[i]), 2)
    print(log)


def generateTFIDFtable():
    print("\nGenerating TFIDF Table...")
    header = ('Search Query', 'Document containing term (df)', 'Total Documents(N)/(df)', 'Log10 (N/df)')
    with open('newsoutput1.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(['Total Documents', str(len(data))])
        writer.writerow(header)
        for i in df:
            writer.writerow([i, df[i], tfidf[i], log[i]])
    print("FINISH")


def getArticleWithHighestOccurrence():
    highest = {
        'count': 0,
        'article': ""
    }
    dataframe = pd.read_csv("newsOutput2.csv")
    for index, each in dataframe.iterrows():
        if each['Frequency'] > highest['count']:
            highest['count'] = each['Frequency']
            highest['article'] = each['Articles']
    print(highest['article'] + " has the highest occurrence")
    return highest


def generateWFTable():
    print(f"\nGenerate Word Frequency Table...")
    header = (
        'Articles', 'TotalWords', 'Frequency')
    with open('newsOutput2.csv', 'w', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(header)
        for i in range(len(data)):
            if data[i]['canada'] > 0:
                writer.writerow(['Article #' + str(i + 1), str(data[i]['wordcount']), str(data[i]['canada'])])
    print("FINISH")


def getHighestRelativeFreq():
    highest = {
        'frequency': 0,
        'article': ""
    }
    dataframe = pd.read_csv("newsOutput2.csv")
    for index, row in dataframe.iterrows():
        if row['Frequency'] / row['TotalWords'] > highest['frequency']:
            highest['frequency'] = row['Frequency'] / row['TotalWords']
            highest['article'] = row['Articles']
    print(highest['article'] + " has the highest relative frequency")
    return highest


if __name__ == '__main__':
    loadnews()
    calculatedf()
    calculateTFIDF()
    calculateLog()
    generateTFIDFtable()
    generateWFTable()
    getArticleWithHighestOccurrence()
    getHighestRelativeFreq()
