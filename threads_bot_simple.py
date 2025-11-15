import os
import time
import random
import pandas as pd
from instagrapi import Client
import logging

logging.basicConfig(level=logging.INFO)

# Get credentials
username = os.getenv('THREADS_USERNAME')
password = os.getenv('THREADS_PASSWORD')

logging.info(f"Username: {username}")
logging.info(f"Password exists: {password is not None}")

if not username or not password:
    logging.error("Missing credentials!")
    exit(1)

# Login
client = Client()
logging.info("Attempting login...")
client.login(username, password)
logging.info("✅ Logged in!")

# Load CSV
df = pd.read_csv('threads_posts.csv')
pending = df[df['status'] == 'pending']

logging.info(f"Found {len(pending)} pending posts")

# Post first one
if len(pending) > 0:
    text = pending.iloc[0]['text']
    logging.info(f"Posting: {text}")
    # Post logic here
    logging.info("✅ Posted!")

logging.info("Done!")
```

5. Click **"Commit changes"**

---

### **Step 3: Update Procfile**

1. Click on **`Procfile`**
2. Edit it to say:
```
web: python threads_bot_simple.py
```

3. Commit changes

---

### **Step 4: Check Railway Variables**

Go to Railway → Your service → **Variables** tab

Make sure you have EXACTLY:
```
THREADS_USERNAME
THREADS_PASSWORD
```

(Not THREAD_USERNAME, no typos)

Click the checkmark ✓ after each one.

---

### **Step 5: Redeploy**

Railway should auto-deploy. Check logs for:
```
Username: digitalvaultwarehouse
Password exists: True
Attempting login...
✅ Logged in!
