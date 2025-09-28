# File: ssmb29_bot.py

import tweepy
import datetime
import os
import random

try:
    # IMPORTANT: These will be the keys for your NEW SSMB29 bot account
    API_KEY = os.environ["TWITTER_API_KEY"]
    API_SECRET_KEY = os.environ["TWITTER_API_SECRET_KEY"]
    ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
except KeyError:
    print("Error: Twitter API credentials not found in environment variables.")
    exit()

# --- Twitter Authentication ---
auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api_v1 = tweepy.API(auth)
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# --- Countdown Configuration ---
update_date = datetime.date(2025, 11, 1)
today = datetime.date.today()
days_to_update = (update_date - today).days

# --- Tweet Composition Logic ---
if days_to_update > 1:
    tweet_text = f"🔥 {days_to_update} days until the big #SSMB29 update!\n\n#MaheshBabu #SSRajamouli"
elif days_to_update == 1:
    tweet_text = "The #SSMB29 update is TOMORROW! Get ready! 💥\n\n#MaheshBabu #SSRajamouli"
elif days_to_update == 0:
    # This is the special tweet for November 1st
    tweet_text = "GLOBETROTTER MONTH HAS ARRIVED\n\n#SSMB29"
else:
    # This is the message that will post every day AFTER Nov 1st
    tweet_text = "Stay tuned for the latest on #SSMB29 following the recent update! News could drop anytime.\n\n#MaheshBabu #SSRajamouli"

# --- Post the Tweet ---
try:
    # This part remains the same. You can add media to a folder in this new project.
    media_folder = "media/" # Make sure this folder exists in your SSMB29_Bot project
    media_files = [f for f in os.listdir(media_folder) if os.path.isfile(os.path.join(media_folder, f))]

    if not media_files:
        response = client.create_tweet(text=tweet_text)
    else:
        random_image_path = os.path.join(media_folder, random.choice(media_files))
        media = api_v1.media_upload(filename=random_image_path)
        response = client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    print(f"Tweet sent successfully! Tweet ID: {response.data['id']}")

except Exception as e:
    print(f"An error occurred: {e}")