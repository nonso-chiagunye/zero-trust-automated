# Create Cloudflare organization and choose a team subdomain name for Warp enrolment

import requests
import sys
sys.path.append('..')
import config 

url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/access/organizations"

data = {
    "allow_authenticate_via_warp": False,
    "auth_domain": "myteam.cloudflareaccess.com", # Your unique organization/team subdomain
    "auto_redirect_to_identity": True,
    "is_ui_read_only": False, # Allow administration via dashboard also 
    "name": "My Organization Name", # Your organization/team name
    "session_duration": "24h", # Token lifespan
    "user_seat_expiration_inactive_time": "730h",
    "warp_auth_session_duration": "24h"
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
        print("Organization created successfully.")
        print("Response data:", response.json())
    else:
        print(f"Failed to create organization: {response.status_code}")
        print("Response content:", response.text)

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")
