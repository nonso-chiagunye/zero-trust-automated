


import requests
import sys
sys.path.append('..')
import config

# Cloudflare API endpoint
url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/teamnet/routes"

# Headers
headers = {
    "Content-Type": "application/json",
    "X-Auth-Email": config.email,
    "X-Auth-Key": config.api_key
}

# Tunnel ID from previous response
tunnel_id = config.tunnel_id  # Tunnel ID from tunnel created earlier

# Payload
data = {
    "network": "x.x.x.x/y",
    "tunnel_id": tunnel_id,
    "comment": "Route to my private network",
}

try:
    # Make the request
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200 and response.json().get("success"):
        route_id = response.json()["result"].get("id")
        print(f"✅ Route Created Successfully! Route ID: {route_id}")
    else:
        print(f"❌ Failed to create route. HTTP {response.status_code}")
        print(f"Error: {response.json().get('errors', 'Unknown error')}")

except requests.exceptions.RequestException as e:
    print(f"⚠️ An error occurred: {e}")
