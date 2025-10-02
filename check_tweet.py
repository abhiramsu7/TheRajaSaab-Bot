import tweepy
import datetime
import os
from zoneinfo import ZoneInfo

API_KEY = os.environ["TWITTER_API_KEY"]
API_SECRET_KEY = os.environ["TWITTER_API_SECRET_KEY"]
ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api_v1 = tweepy.API(auth)
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# --- Countdown Config ---
release_date = datetime.date(2026, 1, 9)
today = datetime.datetime.now(tz=ZoneInfo("Asia/Kolkata")).date()
days_left = (release_date - today).days

if days_left > 1:
    tweet_text = f"{days_left} "
elif days_left == 1:
    tweet_text = "h"
elif days_left == 0:
    tweet_text = "k"
else:
    tweet_text = f"Celebrating {-days_left} day(s) since #Rajasaab's release!"

# --- Check last tweet ---
last_tweet = api_v1.user_timeline(count=1)[0].text if api_v1.user_timeline(count=1) else ""

if last_tweet.strip() == tweet_text.strip():
    print("Tweet already posted today, skipping...")
else:
    print("Posting tweet from GitHub fallback...")
    client.create_tweet(text=tweet_text)
