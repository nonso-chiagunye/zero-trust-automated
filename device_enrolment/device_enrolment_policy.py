import requests
import sys
sys.path.append('..')
import config 

url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/devices/policy"

data = {
    "allow_mode_switch": False,
    "allow_updates": True,
    "allowed_to_leave": False, # Don't allow devices to leave your organization/team
    "auto_connect": 0, 
    "captive_portal": 180, # Idle time to turn on captive portal
    "description": "Device enrolment policy",
    "disable_auto_fallback": True,
    "enabled": True,
    "match": "identity.email in [\"*@mycompany.com\"]", # Allow users with corporate email
    "name": "Device enrolment",
    "precedence": 100,
    "service_mode_v2": {
        "mode": "warp",
    },
    "support_url": "https://it.mycompany.com/help",
    "switch_locked": True, # Mandate user to always be on warp
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
        print("Policy created successfully.")
        response_data = response.json()
        policy_id = response_data["result"]["policy_id"]
        print(f"Policy ID: {policy_id}")
    else:
        print(f"Failed to create policy: {response.status_code}")
        print("Response content:", response.text)

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")


# https://chatgpt.com/c/66f59523-0b3c-8007-9ce6-7d9db1877cb0