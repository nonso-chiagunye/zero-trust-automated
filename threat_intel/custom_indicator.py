# Create custom indicator instance 

# https://developers.cloudflare.com/security-center/indicator-feeds/

import requests
import sys
sys.path.append('..')
import config 

# API endpoint
url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/intel/indicator-feeds"

headers = {
    "Content-Type": "application/json",
    'X-Auth-Email': config.email,
    'X-Auth-Key': config.api_key
}

# Required data
data = {
    "description": "Custom indicator feed to detect threats",
    "name": "threat_indicator_feed"
}

try:
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200 and response.json().get('success'):
        print("Custom indicator created successfully.")
        feed_id = response.json()["result"]["id"]
        print(f"Feed ID: {feed_id}")
    else:
        print(f"Failed to create custom indicator: {response.status_code}")
        print(f"Response content: {response.text}")

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")

