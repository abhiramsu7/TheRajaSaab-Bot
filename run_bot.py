import tweepy
import datetime
import os
import time
from zoneinfo import ZoneInfo
from dotenv import load_dotenv

load_dotenv()
print("Debug: API key from env =", os.getenv("TWITTER_API_KEY"))


# --- Load Twitter credentials from env vars ---
try:
    API_KEY = os.environ["TWITTER_API_KEY"]
    API_SECRET_KEY = os.environ["TWITTER_API_SECRET_KEY"]
    ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
    ACCESS_TOKEN_SECRET = os.environ["TWITTER_ACCESS_TOKEN_SECRET"]
except KeyError:
    print("Error: Twitter API credentials not found in environment variables.")
    exit()

# --- Auth ---
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
today = datetime.datetime.now(tz=ZoneInfo("Asia/Kolkata")).date()

# --- Skip if countdown hasn't started ---
if today < countdown_start_date:
    print(f"Countdown has not started. It begins on {countdown_start_date}.")
    exit()

days_left = (release_date - today).days

# --- Tweet Composition ---
if days_left == 102:  # Trailer release day
    tweet_text = f"{days_left}"
elif days_left == 101:  # Day after trailer
    tweet_text = f"{days_left}"
elif days_left > 1:  # General countdown
    tweet_text = f"{days_left} "
elif days_left == 1:
    tweet_text = "1 day left until #TheRajaSaab release! 💥"
elif days_left == 0:
    tweet_text = "The wait is over! #TheRajaSaab releases today 🎉🔥"
else:
    tweet_text = f"Celebrating {-days_left} day(s) since #TheRajaSaab's release! What are your reviews? #Prabhas"

# --- Check if today's tweet already exists ---
def already_tweeted(snippet):
    try:
        tweets = api_v1.user_timeline(count=20, tweet_mode="extended")
        for t in tweets:
            if snippet in t.full_text:
                return True
    except Exception as e:
        print("⚠️ Warning: Could not fetch timeline:", e)
        return False
    return False

snippet = str(days_left)  # use days_left as unique daily marker

if already_tweeted(snippet):
    print("✔️ Tweet for today already exists. Exiting.")
else:
    try:
        print("Posting a text-only tweet...")
        response = client.create_tweet(text=tweet_text)
        print(f"✅ Tweet sent successfully! Tweet ID: {response.data['id']}")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        exit()

# --- Shutdown logic (only for local Windows Task Scheduler) ---
if os.name == "nt":  # only on Windows
    print("💤 Waiting 20 minutes before shutdown...")
    time.sleep(1200)  # 20 minutes
    print("⚡ Shutting down now...")
    os.system("shutdown /s /t 1")
