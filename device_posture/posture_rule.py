# Create device posture rule 

import requests
import sys
sys.path.append('..')
import config 

# Set the posture_id obtained from the previous API call
posture_id = "My posture id"

# API Endpoint
url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/devices/posture"

# Set the headers
headers = {
    "Content-Type": "application/json",
    'X-Auth-Email': config.email,
    'X-Auth-Key': config.api_key
}

# Define parameters accoring to your organization's unique requirements
data = {
    "description": "Device posture rule",
    "input": {
        "connection_id": posture_id,
        "sensor_config": ">= 90",
        "overall": ">= 90"
    },
    "match": [
        {"platform": "windows"},
        {"platform": "linux"},
        {"platform": "mac"}
    ],
    "name": "Device Posture",
    "schedule": "5m",
    "type": "crowdstrike_s2s"
}

try:
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200 and response.json().get('success'):
        rule_id = response.json()["result"]["id"]
        print(f"Success! Rule ID: {rule_id}")
    else:
        print(f"Request failed with status code: {response.status_code}")
        print(f"Response: {response.text}")

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")
