# Create a tunnel to connect your private services to Cloudflare global network

import requests
import sys
sys.path.append('..')
import config 

url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/cfd_tunnel"

# Headers
headers = {
    "Content-Type": "application/json",
    "X-Auth-Email": config.email,
    "X-Auth-Key": config.api_key
}

# Payload
data = {
    "name": "example-staging-tunnel-01",
    "config_src": "cloudflare",  # Choose local if you want to configure the tunnel at the cloudflared server with YAML
}

try:

  # Make the request
  response = requests.post(url, headers=headers, json=data)

  # Parse the response
  if response.status_code == 200 and response.json().get('success'):
    tunnel_id = response.json()["result"]["id"]
    print(f"Tunnel ID: {tunnel_id}")
  else:
    print(f"Failed to create tunnel: {response.status_code}")
    print(f"Error: {response.json().get('errors', 'Unknown error')}")

except requests.exceptions.RequestException as e:
  print(f"An error occurred: {e}")
