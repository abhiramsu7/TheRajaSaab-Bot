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
    print("Keys are incorrect:")
    exit()

auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api_v1 = tweepy.API(auth)
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

release_date = datetime.date(2026, 1, 9)
countdown_start_date = datetime.date(2025, 10, 1)
today = datetime.date.today()

# if today < countdown_start_date:
#     print(f"Countdown has not started. It begins on {countdown_start_date}.")
#     exit()

days_left = (release_date - today).days

if days_left > 75:
    media_folder = "media/phase1_buildup"
elif 30 <= days_left <= 75:
    media_folder = "media/phase2_themed"
elif 1 < days_left < 30:
    media_folder = "media/phase3_final"
else:
    media_folder = "media/phase4_release"

print(f"Today is {today}. Days left: {days_left}. Using folder: {media_folder}")

if days_left > 1:
    tweet_text = f"{days_left} DAYS TO GO for #Rajasaab! 🔥\n\nThe countdown is ON! ⏳\n\n#Prabhas #RajasaabCountdown"
elif days_left == 1:
    tweet_text = "JUST 1 DAY TO GO! Get ready for the Rebel Star's arrival! #Rajasaab 💥\n\n#Prabhas"
elif days_left == 0:
    tweet_text = "THE DAY IS HERE! #RAJASAAB has been unleashed! 👑\n\nEnjoy the movie! #Prabhas"
else:
    tweet_text = f"Celebrating {-days_left} day(s) since #Rajasaab's release! What are your reviews? #Prabhas"

try:
    # Get a list of all files in the chosen folder
    media_files = [f for f in os.listdir(media_folder) if os.path.isfile(os.path.join(media_folder, f))]

    if not media_files:
        print(f"No media found in {media_folder}. Posting tweet without media.")
        response = client.create_tweet(text=tweet_text)
    else:
        # Pick a random image from the folder
        random_image_path = os.path.join(media_folder, random.choice(media_files))
        print(f"Uploading media: {random_image_path}")
        
        # Upload the media and post the tweet
        media = api_v1.media_upload(filename=random_image_path)
        response = client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    print(f"Tweet sent successfully! Tweet ID: {response.data['id']}")

except Exception as e:
    print(f"An error occurred: {e}")