#!/usr/bin/python
import tweepy
from textblob import TextBlob
import csv
import os


consumer_key = 'CONSUMER_KEY'
consumer_secret = 'CONSUMER_SECRET'

access_token = 'ACCESS_TOKEN'
access_token_secret = 'ACCESS_TOKEN_SECRET'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)
tweets = api.search("Trump", count=100)

dir_path = os.path.dirname(os.path.realpath(__file__))

with open(dir_path + "/analysis.csv", "w") as csv_file:

    spamwriter = csv.writer(csv_file, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for tweet in tweets:
        print(tweet.text)

        analysis = TextBlob(tweet.text)

        if (analysis.sentiment.polarity <= -0.2 or
                analysis.sentiment.polarity >= 0.2):

            spamwriter.writerow([tweet.text, "positive"
                                if analysis.sentiment.polarity > 0
                                else "negative"])
