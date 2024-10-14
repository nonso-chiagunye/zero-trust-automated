import requests
import sys
sys.path.append('..')
import config 

dlp_profile_id = "<Custom DLP Profile ID created earlier>"

# API Endpoint
url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/gateway/rules"

# Cloudflare API headers
headers = {
    "Content-Type": "application/json",
    'X-Auth-Email': config.email,
    'X-Auth-Key': config.api_key
}

# API Parameters
data = {
    "action": "block",  # Action when the rule matches, can also be "allow", "monitor", etc.
    "description": "Block traffic matching DLP profile",
    "enabled": True,  # Enable the rule
    "filters": [
        "http"  # This can be "http", "dns", or "l4"
    ],
    "name": "DLP Gateway Rule",
    "precedence": 0,  # The priority of the rule; lower numbers mean higher priority
    "traffic": f"any(dlp.profiles[*] in \"{dlp_profile_id}\")"  # Use the custom DLP profile's UUID
}

try:
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200 and response.json().get('success'):
        print("DLP gateway rule created successfully.")
        print(f"Response data: {response.json()}")
    else:
        print(f"Failed to create dlp gateway rule: {response.status_code}")
        print(f"Response content: {response.text}")

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")
