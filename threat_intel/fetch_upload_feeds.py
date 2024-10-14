# Fetch threat data from a threat intel provider (eg spamhaus) and upload to Cloudflare

import requests
import sys
sys.path.append('..')
import config 
import uuid
import json
from datetime import datetime

feed_id = "<YOUR FEED ID>" # Feed ID generated from previous custom feed

# Function to fetch threat feeds from spamhaus 
def fetch_threat_feed():
    url = "https://www.spamhaus.org/drop/drop.txt"  # URL of the DROP list
    response = requests.get(url)
    
    if response.status_code == 200:
        drop_list = response.text.splitlines()
        return drop_list
    else:
        print("Failed to fetch Spamhaus DROP list")
        return []

# Fetch the DROP list
threat_feed = fetch_threat_feed()

# Function to convert threat feeds to stixx 2.0 format 
def convert_threat_feed_to_stix(ip_list):
    stix_bundle = {
        "type": "bundle",
        "id": f"bundle--{uuid.uuid4()}",
        "objects": []
    }

    for ip in ip_list:
        stix_object = {
            "type": "indicator",
            "id": f"indicator--{uuid.uuid4()}",
            "created": datetime.now(datetime.timezone.utc).isoformat() + "Z",
            "modified": datetime.now(datetime.timezone.utc).isoformat() + "Z",
            "pattern": f"[ipv4-addr:value = '{ip}']",
            "valid_from": datetime.now(datetime.timezone.utc).isoformat() + "Z"
        }
        stix_bundle["objects"].append(stix_object)

    return stix_bundle

# Convert the Spamhaus DROP list into STIX format
stix_data = convert_threat_feed_to_stix(threat_feed)

# Save the STIX data to a file
with open("threat_feed.stix2", "w") as stix_file:
    json.dump(stix_data, stix_file, indent=4)

print("STIX threat feed saved.")

# Function to upload stixx file to Cloudflare 
def upload_to_cloudflare(filepath):
    url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/intel/indicator-feeds/{feed_id}/snapshot"

    headers = {        
        "Content-Type": "application/json",
        'X-Auth-Email': config.email,
        'X-Auth-Key': config.api_key
    }
    
    with open(filepath, "rb") as file:
        files = {"source": ("threat_feed.stix2", file, "application/json")}
        response = requests.put(url, headers=headers, files=files)
    
    if response.status_code == 200:
        print("Threat feed successfully uploaded to Cloudflare.")
    else:
        print("Failed to upload threat feed:", response.status_code, response.text)

# Upload the STIX file to Cloudflare
upload_to_cloudflare("threat_feed.stix2")
