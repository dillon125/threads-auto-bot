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

client = Client()
session_file = "session.json"

logging.info("Attempting login...")

try:
    if os.path.exists(session_file):
        logging.info("Loading saved session...")
        client.load_settings(session_file)
        client.login(username, password)
    else:
        logging.info("New login required...")
        client.login(username, password)
        client.dump_settings(session_file)
    
    logging.info("Logged in successfully!")
    
except Exception as e:
    logging.error(f"Login failed: {e}")
    logging.error("You may need to verify your account on Instagram first")
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
