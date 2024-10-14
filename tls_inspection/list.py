# Create a list of IPs to exclude from tls inspection 

import csv
import requests
import sys
sys.path.append('..')
import config 

# API endpoint 
url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/gateway/lists"

# Headers
headers = {
    "Content-Type": "application/json",
    'X-Auth-Email': config.email,
    'X-Auth-Key': config.api_key
}

description = 'Penetration testing IPs'
list_name = 'Pentest IPs'
list_type = 'IP'

# Read IPs from CSV
csv_file = 'ips.csv'
ips = []

with open(csv_file, newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        ip_value = row['IP']
        ips.append({'value': ip_value})

# Create the payload
data = {
    'description': description,
    'items': ips,
    'name': list_name,
    'type': list_type
}

try:
    # Send the POST request to create the IP list
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200 and response.json().get('success'):
        print('IP list created successfully!')
        list_id = response.json()["result"]["id"]
        print(f"List id: {list_id}")
    else:
        print(f'Failed to create IP list. Status code: {response.status_code}')
        print(f'Response: {response.text}')

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")

