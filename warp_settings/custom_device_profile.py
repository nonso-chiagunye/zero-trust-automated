# Create Custom Device Profile. 

import requests
import sys
sys.path.append('..')
import config

# Cloudflare API endpoint
url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/devices/policy"

# Headers
headers = {
    "Content-Type": "application/json",
    "X-Auth-Email": config.email,
    "X-Auth-Key": config.api_key
}

# Payload
data = {
    "match": 'identity.groups.name[*] in {\\"developer\\"}',
    "name": "Developers-Profile",
    "precedence": 100,
    "allow_mode_switch": False,
    "allow_updates": True,
    "allowed_to_leave": False,
    "captive_portal": 180,
    "description": "Device profile for developers.",
    "disable_auto_fallback": True,
    "doh_in_tunnel": True,
    "enabled": True,
    "exclude_office_ips": True,
    "lan_allow_minutes": 30,
    "lan_allow_subnet_size": 24,
    # "register_interface_ip_with_dns": True,
    "support_url": "https://example.com/help",
    "switch_locked": True,
    "tunnel_protocol": "wireguard"
}

try:
    # Make the request
    response = requests.post(url, headers=headers, json=data)
    response_json = response.json()

    if response.status_code == 201 and response_json.get("success"):
        developers_profile = response_json["result"].get("policy_id")
        print(f"✅ Device Profile Created Successfully! Policy ID: {developers_profile}")
    else:
        print(f"❌ Failed to create device profile. HTTP {response.status_code}")
        print(f"Error: {response_json.get('errors', 'Unknown error')}")

except requests.exceptions.RequestException as e:
    print(f"⚠️ An error occurred: {e}")
