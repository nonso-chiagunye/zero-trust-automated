# Defines list of IPs to be excluded from tunneliing through Cloudflare network.

import csv
import requests
import sys
sys.path.append('..')
import config

policy_id = "your_policy_id_here"  # Policy ID from device enrolment policy

url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/devices/policy/{policy_id}/exclude"

headers = {
    "Content-Type": "application/json",
    'X-Auth-Email': config.email,
    'X-Auth-Key': config.api_key
}

# List to hold IP exclusion data
exclude_data = []

# Read data from CSV file (exclude-ips.csv)
csv_file = 'exclude-ips.csv'

with open(csv_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        # Append each row from the CSV as a dictionary
        exclude_data.append({
            "address": row['Address'],
            "description": row['Description']
        })

# Send the PUT request to update the exclude list for the policy
# response = requests.put(url, headers=headers, data=json.dumps(exclude_data))

try:
    # Make the POST request
    response = requests.put(url, headers=headers, json=exclude_data)

    # Check if the request was successful
    if response.status_code == 200 and response.json().get('success'):
        print(f"Successfully updated exclusion list for policy: {policy_id}")
        print(f"Response data: {response.json()}")
    else:
        print(f"Failed to update exclusion list for policy: {policy_id}")
        print(f"Response content: {response.text}")

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")