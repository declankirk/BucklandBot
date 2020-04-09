import markovify
import random
import tweepy
import schedule
import time
from datetime import datetime
from config import consumer_key, consumer_secret, access_key, access_secret

# Get raw text as string.
with open("tweets.txt", encoding="utf8") as f:
    tweets = f.read()
with open("transcripts.txt", encoding="utf8") as f:
    transcripts = f.read()
with open("blogs.txt", encoding="utf8") as f:
    blogs = f.read()
with open("interviews.txt", encoding="utf8") as f:
    interviews = f.read()


# Build the model.
transcripts_model = markovify.NewlineText(transcripts, state_size=2, well_formed = False)
tweets_model = markovify.Text(tweets)
blogs_model = markovify.Text(blogs)
interviews_model = markovify.Text(interviews)

combo_model = markovify.combine([ blogs_model, interviews_model ])
combo_model = markovify.combine([ combo_model, tweets_model ])

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

def job():
    tweet = combo_model.make_short_sentence(280, tries=100).capitalize()
    print()
    print(tweet)
    api.update_status(tweet)
    print("POSTED at", datetime.now())
    print()

if __name__ == '__main__':
    schedule.every(30).to(180).minutes.do(job).run()
    while True:
        schedule.run_pending()
        time.sleep(1)