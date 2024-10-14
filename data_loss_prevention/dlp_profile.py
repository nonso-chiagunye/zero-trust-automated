
import requests
import sys
sys.path.append('..')
import config 

# FETCH PREDEFINED PROFILE BY ITS ID

def fetch_predefined_profile(profile_id, headers):
    url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/dlp/profiles/predefined/{profile_id}"

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200 and response.json().get('success'):
        return response.json()
    else:
        print(f"Failed to retrieve predefined profile {profile_id}: {response.status_code}")
        return None

# Cloudflare API headers
headers = {
    "Content-Type": "application/json",
    'X-Auth-Email': config.email,
    'X-Auth-Key': config.api_key
}

# List of predefined profile IDs you want to fetch (replace with actual profile IDs)
predefined_profile_ids = [
    "profile_id_1",  # Credentials and Secrets
    "profile_id_2",  # Financial Information
    "profile_id_3",  # Health Information
    "profile_id_4"   # National Identifiers
]

# EXTRACT SHARED ENTRIES (id, type) FROM THE PREDEFINED PROFILES

shared_entries = []

for profile_id in predefined_profile_ids:
    profile = fetch_predefined_profile(profile_id, headers)
    
    if profile:
        # Extract shared entry information (id and type) from the profile's entries
        for entry in profile['result']['entries']:
            shared_entry = {
                "enabled": True,
                "entry_id": entry['id'],
                "entry_type": entry['type']
            }
            shared_entries.append(shared_entry)

# CREATE CUSTOM PROFILE BY COMBINING YOUR CUSTOM DEFINED ENTRIES WITH PREDEFINED (SHARED) ENTRIES

url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/dlp/profiles/custom"

data = {
    "profiles": [
        {
            "allowed_match_count": 5,
            "context_awareness": {
                "enabled": True,
                "skip": {
                    "files": True
                }
            },
            "description": "Custom DLP profile",
            "entries": [
                {
                    "enabled": True,
                    "name": "Block @hacker.com emails",
                    "pattern": {
                        "regex": "^[a-zA-Z0-9._%+-]+@hacker\.com$", # Example regex for email pattern
                        "validation": "none"
                    }
                }
            ],
            "name": "CustomDLPProfile",
            "ocr_enabled": True,
            "shared_entries": shared_entries # Use the consolidated shared entries from all predefined profiles
        }
    ]
}

# POST THE CUSTOM DLP PROFILE WITH THE SHARED ENTRIES

try:
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200 and response.json().get('success'):
        print("Custom DLP profile created successfully.")
        dlp_profile_id = response.json()["result"][0]["id"]
        print(f"DLP profile ID: {dlp_profile_id}")
    else:
        print(f"Failed to create custom dlp profile: {response.status_code}")
        print(f"Response content: {response.text}")

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")
