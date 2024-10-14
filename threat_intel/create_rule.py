# Create a gateway rule with your custom indicator feed

import requests
import sys
sys.path.append('..')
import config 

feed_id = "<YOUR FEED ID>" # Feed ID generated from previous custom feed

# API endpoint
url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/gateway/rules"

# Rule parameters
data = {
    "action": "block",
    "description": "Block threats in indicator feed.",
    "enabled": True,
    "filters": ["dns"],
   # "identity": "any(identity.groups.name[*] in {\"finance\"})",
    "name": "indicator rule",
    "precedence": 0,
    "rule_settings": {
        "ip_indicator_feeds": True 
    },

    "traffic": f"any(indicator.feeds[*] in \"{feed_id}\")"
}

headers = {
    "Content-Type": "application/json",
    'X-Auth-Email': config.email,
    'X-Auth-Key': config.api_key
}

try:
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200 and response.json().get('success'):
        print("Indicator gateway rule created successfully.")        
    else:
        print(f"Failed to create rule: {response.status_code} - {response.text}")

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")
