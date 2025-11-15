import os
import time
import random
import pandas as pd
from instagrapi import Client
import logging
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# Debug: Print ALL environment variables
logging.info("All environment variables:")
for key in os.environ:
    if 'THREADS' in key:
        logging.info(f"{key}: {os.environ[key][:5]}...")

# Get credentials with fallback
username = os.environ.get('THREADS_USERNAME', '')
password = os.environ.get('THREADS_PASSWORD', '')

logging.info(f"Username: '{username}'")
logging.info(f"Password length: {len(password)}")

if not username or not password:
    logging.error("Missing credentials!")
    logging.error(f"USERNAME empty: {not username}")
    logging.error(f"PASSWORD empty: {not password}")
    sys.exit(1)

client = Client()
logging.info("Attempting login...")
client.login(username, password)
logging.info("✅ Logged in successfully!")

df = pd.read_csv('threads_posts.csv')
pending = df[df['status'] == 'pending']

logging.info(f"Found {len(pending)} pending posts")

if len(pending) > 0:
    text = pending.iloc[0]['text']
    logging.info(f"Posting: {text[:50]}...")
    
logging.info("Bot completed!")
time.sleep(86400)
