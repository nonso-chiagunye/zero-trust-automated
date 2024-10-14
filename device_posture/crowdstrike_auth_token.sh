#!/bin/bash

# This request enables Cloudflare Zero Trust to add Crowdstrike as a service provider, thereby getting device posture data from the defined client endpoint. 
# https://developers.cloudflare.com/cloudflare-one/identity/devices/service-providers/crowdstrike/

# Get necessary credentials from secret file
BASE_URL=$(grep 'crowdstrike_base_url' ../config.py | awk -F' = ' '{print $2}' | tr -d '"')
CLIENT_ID=$(grep 'crowdstrike_client_id' ../config.py | awk -F' = ' '{print $2}' | tr -d '"')
CLIENT_SECRET=$(grep 'crowdstrike_client_secret' ../config.py | awk -F' = ' '{print $2}' | tr -d '"')

# Make the post request
response=$(curl -s -X POST "$BASE_URL/oauth2/token" \
    -H "accept: application/json" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "client_id=$CLIENT_ID&client_secret=$CLIENT_SECRET")

# Check for success or failure
if [ $? -eq 0 ]; then
    echo "Provider enabled."
    echo "Response: $response"
    exit 0
else
    echo "Failed to enable provider."
    echo "Response: $response"
    exit 1
fi

