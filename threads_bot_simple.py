import os
import time
import random
import pandas as pd
from instagrapi import Client
import logging
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

username = "digitalvaultwarehouse"
password = "Milly123456!!"

logging.info(f"Using username: {username}")

client = Client()
logging.info("Attempting login...")

try:
    client.login(username, password)
    logging.info("Logged in successfully!")
except Exception as e:
    logging.error(f"Login failed: {e}")
    sys.exit(1)

try:
    df = pd.read_csv('threads_posts.csv')
    pending = df[df['status'] == 'pending']
    
    logging.info(f"Found {len(pending)} pending posts")
    
    if len(pending) > 0:
        text = pending.iloc[0]['text']
        logging.info(f"Ready to post: {text[:50]}...")
        
    logging.info("Bot working!")
    
except Exception as e:
    logging.error(f"Error: {e}")

time.sleep(86400)
