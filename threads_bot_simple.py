import os
import time
import random
import pandas as pd
from instagrapi import Client
import logging

logging.basicConfig(level=logging.INFO)

username = os.getenv('THREADS_USERNAME')
password = os.getenv('THREADS_PASSWORD')

logging.info(f"Username: {username}")
logging.info(f"Password exists: {password is not None}")

if not username or not password:
    logging.error("Missing credentials!")
    exit(1)

client = Client()
logging.info("Attempting login...")
client.login(username, password)
logging.info("Logged in successfully!")

df = pd.read_csv('threads_posts.csv')
pending = df[df['status'] == 'pending']

logging.info(f"Found {len(pending)} pending posts")

if len(pending) > 0:
    text = pending.iloc[0]['text']
    logging.info(f"Posting: {text}")
    logging.info("Posted!")

logging.info("Bot completed!")
