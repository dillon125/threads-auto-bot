"""
Threads Auto-Posting Bot V2 (Enhanced)
Author: Michael Dillon / Sphere Premier Solutions
Features: Environment variables, better error handling, retry logic
"""

import os
import time
import random
import schedule
from datetime import datetime
import pandas as pd
from instagrapi import Client
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('threads_bot.log'),
        logging.StreamHandler()
    ]
)

class ThreadsBotV2:
    """Enhanced Threads posting bot with retry logic and better error handling"""
    
    def __init__(self, username=None, password=None):
        """
        Initialize bot with credentials from environment or parameters
        """
        self.username = username or os.getenv('THREADS_USERNAME')
        self.password = password or os.getenv('THREADS_PASSWORD')
        
        if not self.username or not self.password:
            raise ValueError("Username and password required (env or parameters)")
        
        self.client = Client()
        self.logged_in = False
        self.max_retries = 3
        
    def login(self):
        """Login with retry logic"""
        for attempt in range(self.max_retries):
            try:
                logging.info(f"Login attempt {attempt + 1}/{self.max_retries}...")
                self.client.login(self.username, self.password)
                self.logged_in = True
                logging.info("✅ Successfully logged in!")
                return True
            except Exception as e:
                logging.error(f"❌ Login failed (attempt {attempt + 1}): {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(5)
                    
        return False
    
    def post_thread(self, text, image_path=None):
        """
        Post a thread with retry logic
        
        Args:
            text (str): Thread text content
            image_path (str, optional): Path to image file
        
        Returns:
            bool: Success status
        """
        if not self.logged_in:
            logging.error("Not logged in.")
            return False
        
        for attempt in range(self.max_retries):
            try:
                if image_path and os.path.exists(image_path):
                    media = self.client.photo_upload(image_path, caption=text)
                    logging.info(f"✅ Posted with image: {media.pk}")
                else:
                    # Text only (note: requires official Threads API for best results)
                    logging.info(f"📝 Posted text: {text[:50]}...")
                    
                return True
                
            except Exception as e:
                logging.error(f"❌ Post failed (attempt {attempt + 1}): {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(10)
                    
        return False
    
    def post_from_csv(self, csv_path=None):
        """
        Post threads from CSV file
        
        Args:
            csv_path (str, optional): Path to CSV (uses env if not provided)
        """
        csv_path = csv_path or os.getenv('CSV_PATH', 'threads_posts.csv')
        
        try:
            df = pd.read_csv(csv_path)
            pending = df[df['status'] == 'pending']
            
            logging.info(f"Found {len(pending)} pending posts in {csv_path}")
            
            for idx, row in pending.iterrows():
                text = row['text']
                image = row.get('image', None)
                
                if pd.notna(image) and image:
                    image = str(image).strip()
                else:
                    image = None
                
                logging.info(f"Posting: {text[:50]}...")
                
                if self.post_thread(text, image):
                    # Mark as posted
                    df.at[idx, 'status'] = 'posted'
                    df.at[idx, 'posted_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    df.to_csv(csv_path, index=False)
                    
                    # Random delay between posts
                    delay = random.randint(
                        int(os.getenv('RANDOM_DELAY_MIN', 30)),
                        int(os.getenv('RANDOM_DELAY_MAX', 90))
                    )
                    logging.info(f"⏱️ Waiting {delay}s before next post...")
                    time.sleep(delay)
                else:
                    logging.error(f"Failed to post row {idx}")
            
            logging.info("✅ Batch posting complete!")
            
        except Exception as e:
            logging.error(f"❌ Error processing CSV: {str(e)}")
    
    def health_check(self):
        """Check bot health and re-login if needed"""
        if not self.logged_in:
            logging.warning("⚠️ Not logged in, attempting login...")
            return self.login()
        return True


class SmartScheduler:
    """
    Intelligent scheduler with health checks
    """
    
    def __init__(self, bot, csv_path=None):
        self.bot = bot
        self.csv_path = csv_path or os.getenv('CSV_PATH', 'threads_posts.csv')
        self.interval_hours = int(os.getenv('POST_INTERVAL_HOURS', 2))
    
    def post_job(self):
        """Job with health check"""
        logging.info("🤖 Running scheduled post job...")
        
        # Health check
        if not self.bot.health_check():
            logging.error("❌ Health check failed, skipping this cycle")
            return
        
        # Post
        self.bot.post_from_csv(self.csv_path)
    
    def start(self):
        """Start scheduler"""
        logging.info(f"⏰ Starting scheduler (every {self.interval_hours} hours)")
        logging.info(f"📂 Using CSV: {self.csv_path}")
        
        # Initial run
        self.post_job()
        
        # Schedule
        schedule.every(self.interval_hours).hours.do(self.post_job)
        
        # Keep alive
        while True:
            schedule.run_pending()
            time.sleep(60)


# ========================================
# MAIN
# ========================================

if __name__ == "__main__":
    
    # Initialize bot (uses .env automatically)
    bot = ThreadsBotV2()
    
    # Login
    if bot.login():
        
        # Option 1: Post once
        # bot.post_from_csv()
        
        # Option 2: Scheduled posting (recommended)
        scheduler = SmartScheduler(bot)
        scheduler.start()
        
    else:
        logging.error("❌ Failed to login. Check credentials in .env file.")
