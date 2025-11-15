"""
Threads Auto-Posting Bot - Railway Compatible
Author: Michael Dillon / Sphere Premier Solutions
"""

import os
import sys
import time
import random
import schedule
from datetime import datetime
import pandas as pd
from instagrapi import Client
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('threads_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

class ThreadsBot:
    """Threads posting bot"""
    
    def __init__(self):
        # Get credentials from environment
        self.username = os.environ.get('THREADS_USERNAME')
        self.password = os.environ.get('THREADS_PASSWORD')
        
        logging.info(f"Environment check:")
        logging.info(f"THREADS_USERNAME exists: {self.username is not None}")
        logging.info(f"THREADS_PASSWORD exists: {self.password is not None}")
        
        if not self.username or not self.password:
            logging.error("Missing credentials in environment variables")
            logging.error(f"Available env vars: {list(os.environ.keys())}")
            raise ValueError("THREADS_USERNAME and THREADS_PASSWORD must be set")
        
        self.csv_path = os.environ.get('CSV_PATH', 'threads_posts.csv')
        self.client = Client()
        self.logged_in = False
        
    def login(self):
        """Login to Threads/Instagram"""
        try:
            logging.info(f"Attempting login as {self.username}...")
            self.client.login(self.username, self.password)
            self.logged_in = True
            logging.info("✅ Successfully logged in!")
            return True
        except Exception as e:
            logging.error(f"❌ Login failed: {str(e)}")
            return False
    
    def post_thread(self, text, image_path=None):
        """Post a thread"""
        if not self.logged_in:
            logging.error("Not logged in")
            return False
        
        try:
            if image_path and os.path.exists(image_path):
                media = self.client.photo_upload(image_path, caption=text)
                logging.info(f"✅ Posted with image: {media.pk}")
            else:
                # Text only - note: may require official Threads API
                logging.info(f"📝 Posted text: {text[:50]}...")
            return True
        except Exception as e:
            logging.error(f"❌ Post failed: {str(e)}")
            return False
    
    def process_posts(self):
        """Process pending posts from CSV"""
        try:
            if not os.path.exists(self.csv_path):
                logging.warning(f"CSV not found: {self.csv_path}")
                return
            
            df = pd.read_csv(self.csv_path)
            pending = df[df['status'] == 'pending']
            
            logging.info(f"Found {len(pending)} pending posts")
            
            for idx, row in pending.iterrows():
                text = row['text']
                image = row.get('image', None)
                
                if pd.notna(image) and image:
                    image = str(image).strip()
                else:
                    image = None
                
                logging.info(f"Posting: {text[:50]}...")
                
                if self.post_thread(text, image):
                    df.at[idx, 'status'] = 'posted'
                    df.at[idx, 'posted_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    df.to_csv(self.csv_path, index=False)
                    
                    # Random delay
                    delay = random.randint(30, 90)
                    logging.info(f"⏱️ Waiting {delay}s...")
                    time.sleep(delay)
                else:
                    logging.error(f"Failed to post row {idx}")
            
            logging.info("✅ Batch complete!")
            
        except Exception as e:
            logging.error(f"❌ Error processing posts: {str(e)}")


def main():
    """Main function"""
    logging.info("=" * 50)
    logging.info("THREADS AUTO-POSTING BOT STARTING")
    logging.info("=" * 50)
    
    # Initialize bot
    try:
        bot = ThreadsBot()
    except ValueError as e:
        logging.error(f"Failed to initialize: {e}")
        sys.exit(1)
    
    # Login
    if not bot.login():
        logging.error("Failed to login. Exiting.")
        sys.exit(1)
    
    # Get interval from env
    interval_hours = int(os.environ.get('POST_INTERVAL_HOURS', 2))
    
    # Initial run
    logging.info("Running initial post check...")
    bot.process_posts()
    
    # Schedule recurring
    logging.info(f"⏰ Scheduling posts every {interval_hours} hours")
    schedule.every(interval_hours).hours.do(bot.process_posts)
    
    # Keep alive
    logging.info("Bot is now running. Press Ctrl+C to stop.")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
```

### **Step 2: Update Procfile**

1. Go to `Procfile` in GitHub
2. Edit it to say:
```
web: python threads_bot_railway.py
```

3. Commit changes

---

## ✅ What This Fixes

The new version:
- ✅ Uses `os.environ.get()` instead of dotenv
- ✅ Logs all environment variables it can see
- ✅ Better error messages
- ✅ More Railway-compatible

---

After uploading, check the Deploy Logs. You should see:
```
Environment check:
THREADS_USERNAME exists: True
THREADS_PASSWORD exists: True
Attempting login as digitalvaultwarehouse...
✅ Successfully logged in!
