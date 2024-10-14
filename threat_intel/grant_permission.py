# Grant subscribers permission to an indicator feed

import requests
import sys
sys.path.append('..')
import config 

subscriber_account_tag = "<SUBSCRIBER ACCOUNT DETAILS>"  # Subscriber's account tag
feed_id = "<YOUR FEED ID>" # Feed ID generated from previous custom feed

# API endpoint
url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/intel/indicator-feeds/permissions/add"

# Cloudflare headers
headers = {
    "Content-Type": "application/json",
    'X-Auth-Email': config.email,
    'X-Auth-Key': config.api_key
}

# Required parameters
data = {
    "account_tag": subscriber_account_tag,
    "feed_id": feed_id
}

try:
    # Make the POST request
    response = requests.put(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200 and response.json().get('success'):
        print("Permission granted successfully.")        
    else:
        print(f"Failed to grant permission: {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")
