# Integrate Crowdstrike for device posture data

import requests
import sys
sys.path.append('..')
import config 

# API Endpoint
url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/devices/posture/integration"

# Cloudflare Auth headers
headers = {
    "Content-Type": "application/json",
    'X-Auth-Email': config.email,
    'X-Auth-Key': config.api_key
}

# Parameters required by Crowdstrike
data = {
    "config": {
        "api_url": "https://api.us-2.crowdstrike.com",
        "customer_id": config.crowdstrike_customer_id,
        "client_id": config.crowdstrike_client_id,
        "client_secret": config.crowdstrike_client_secret
    },
    "interval": "5m", # Refresh time to poll new device pposture data
    "name": "My Crowdstrike Integration",
    "type": "crowdstrike_s2s"
}

try:
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200 and response.json().get('success'):
        posture_id = response.json()["result"]["id"]
        print(f"Success! Posture ID: {posture_id}")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response: {response.text}")

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")
