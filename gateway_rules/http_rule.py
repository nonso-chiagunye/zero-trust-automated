
import requests
import json 
import sys
sys.path.append('..')
import config

# Define the API endpoint URL and headers
url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/gateway/rules"

headers = {
    'Content-Type': 'application/json',
    'X-Auth-Email': config.email,
    'X-Auth-Key': config.api_key  
}

# Define the payload (data) for the POST request
data = {
    "action": "block",
    "description": "Block malicious website.",
    "enabled": True,
    "filters": [
        "http"
    ],
    "name": "Malicious website",
    "precedence": 0,
    "rule_settings": {
        "allow_child_bypass": False,
        "block_page_enabled": True,
        "block_reason": "This website is a security risk",
        "resolve_dns_through_cloudflare": True
    },
    "traffic": "http.request.uri matches \".*a/partial/uri.*\" and http.request.host in $01302951-49f9-47c9-a400-0297e60b6a10" 
}

try:
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200 and response.json().get('success'):
        print("HTTP rule created successfully.")
        print("Response data:", response.json())
    else:
        print(f"Failed to create dns rule. Errors: {response.status_code}")
        print("Response content:", response.text)

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")

