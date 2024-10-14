# Create do not inspect rule for pentest ips

import requests
import sys
sys.path.append('..')
import config 

list_id = "<YOUR LIST ID>" # Generated from list profile

# API endpoint
url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/gateway/rules"

# Headers
headers = {
    "Content-Type": "application/json",
    'X-Auth-Email': config.email,
    'X-Auth-Key': config.api_key
}

# Do not inspect configuration 
data = {
    "name": "Do not inspect pentest ips",
    "conditions": [
        {
            "type": "device_posture",
            "expression": {
                "any": {
                    "in": {
                        "lhs": {
                            "splat": "device_posture.checks.passed"
                        },
                        "rhs": [
                            list_id
                        ]
                    }
                }
            }
        }
    ],
    "action": "off",
    "precedence": 1,
    "enabled": True,
    "filters": [
        "l4"
    ]
}

try:
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200 and response.json().get('success'):
        print("Do not inspect policy created successfully.")
    else:
        print(f"Failed to create do not inspect policy: {response.status_code}")

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")
