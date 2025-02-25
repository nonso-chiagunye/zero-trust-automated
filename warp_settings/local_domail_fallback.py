# Create Local Domain Fallback to resolve internal domains

import requests
import sys
sys.path.append('..')
import config

url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/devices/policy/{config.developers_profile}/fallback_domains"

# Headers
headers = {
    "Content-Type": "application/json",
    "X-Auth-Email": config.email,
    "X-Auth-Key": config.api_key
}

# Payload
data = [
    {
        "suffix": "example-internal-domain.com",
        "description": "Domain bypass for local development",
        "dns_server": [
            "x.x.x.x"
        ]
    }
]

try:
    response = requests.put(url, headers=headers, json=data)
    response_json = response.json()

    if response.status_code == 200 and response_json.get("success"):
        print("✅ Fallback domains updated successfully!")
    else:
        print(f"❌ Failed to update fallback domains. HTTP {response.status_code}")
        print(f"Error: {response_json.get('errors', 'Unknown error')}")

except requests.exceptions.RequestException as e:
    print(f"⚠️ An error occurred: {e}")
