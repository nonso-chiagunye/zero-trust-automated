# Create gateway rule with the device posture rule

import requests
import sys
sys.path.append('..')
import config 

rule_id = "<Device posture rule id>" # Replace with the actual rule_id obtained from the previous response

# Define the API endpoint URL and headers
url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/gateway/rules"

headers = {
    "Content-Type": "application/json",
    'X-Auth-Email': config.email,
    'X-Auth-Key': config.api_key
}

# Define the payload (data) for the POST request
data = {
    "action": "block",
    "description": "Failed Posture Check",
    "enabled": True,
    "filters": [
        "l4"
    ],
    "name": "Failed Posture Check",
    "precedence": 0,
    "rule_settings": {
        "allow_child_bypass": False,
        "block_page_enabled": True,
        "block_reason": "Device posture check failed",
    },
    "traffic": f'any(device_posture.checks.failed[*] in {{"{rule_id}"}})'
}

try:
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200 and response.json().get('success'):
        print("DLP gateway rule created successfully.")
        print(f"Response data: {response.json()}")
    else:
        print(f"Failed to create dlp gateway rule. Errors: {response.status_code}")
        print(f"Response content: {response.text}")

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")