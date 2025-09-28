import tweepy
import datetime
import os
import random

try:
    API_KEY = os.environ["TWITTER_API_KEY"]
    API_SECRET_KEY = os.environ["TWITTER_API_SECRET_KEY"]
    ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
except KeyError:
    print("Error: Twitter API credentials not found in environment variables.")
    exit()

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api_v1 = tweepy.API(auth)
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# --- Countdown Configuration ---
release_date = datetime.date(2026, 1, 9)
countdown_start_date = datetime.date(2025, 9, 29)
today = datetime.date.today()

# --- Main Script Logic ---
if today < countdown_start_date:
    print(f"Countdown has not started. It begins on {countdown_start_date}.")
    exit()

days_left = (release_date - today).days

# --- Tweet Composition Logic ---
if days_left == 102: # Specifically for Sept 29th (Trailer Release Day)
    tweet_text = f"THE COUNTDOWN BEGINS! 🔥 {days_left} ! The official trailer drops this evening! "
elif days_left == 101: # Specifically for Sept 30th (Day after trailer)
    tweet_text = f"Did you see the trailer?! 💥 {days_left} "
elif days_left > 1: # General countdown for all other days
    tweet_text = f"{days_left} "
elif days_left == 1:
    tweet_text = "JUST 1 DAY TO GO! Get ready for the Rebel Star's arrival! "
elif days_left == 0:
    tweet_text = "THE DAY IS HERE! #RAJASAAB has been unleashed! "
else:
    tweet_text = f"Celebrating {-days_left} day(s) since #Rajasaab's release! What are your reviews? #Prabhas"


# --- Post the Tweet (Text Only) ---
try:
    print("Posting a text-only tweet...")
    response = client.create_tweet(text=tweet_text)
    print(f"Tweet sent successfully! Tweet ID: {response.data['id']}")
except Exception as e:
    print(f"An error occurred: {e}")