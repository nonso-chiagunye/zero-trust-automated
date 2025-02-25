# Create split tunnel and specify Ip or Doamin that should not be routed through Cloudflare Gateway 

import requests
import sys
sys.path.append('..')
import config

url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/devices/policy/{config.developers_profile}/exclude"

# Headers
headers = {
    "Content-Type": "application/json",
    "X-Auth-Email": config.email,
    "X-Auth-Key": config.api_key
}

# Payload
data = [
    {
        "address": "192.0.2.0/24",
        "description": "Exclude testing domains from the tunnel",
        "host": "*.example.com"
    }
]

try:
    response = requests.put(url, headers=headers, json=data)
    response_json = response.json()

    if response.status_code == 200 and response_json.get("success"):
        print("✅ Exclude list updated successfully!")
    else:
        print(f"❌ Failed to update exclude list. HTTP {response.status_code}")
        print(f"Error: {response_json.get('errors', 'Unknown error')}")

except requests.exceptions.RequestException as e:
    print(f"⚠️ An error occurred: {e}")
