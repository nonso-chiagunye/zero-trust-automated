#!/bin/bash

# Schdule cron to fetch threat feeds and upload to Cloadflare every 10am

# Define the cron schedule (every day at 10 AM)
CRON_SCHEDULE="0 10 * * *"

# Path to the Python script
SCRIPT_PATH="$HOME/threats/fetch_upload_feeds.py"

# Cron command
CRON_CMD="python3 $SCRIPT_PATH"

# Check if the cron job already exists
(crontab -l | grep -v "$SCRIPT_PATH"; echo "$CRON_SCHEDULE $CRON_CMD") | crontab -

echo "Cron job for fetch_upload_feeds.py has been set to run daily at 10 AM."

# chmod +x setup_cron.sh
# ./setup_cron.sh
