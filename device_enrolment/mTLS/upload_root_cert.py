# Uploads the generated root certificate  to Cloudlfare

import os
import requests
import sys
sys.path.append('../..')
import config 

# Directory where the certificate and key files are located
root_ca_dir = "root-ca"

# File paths for the CA certificate and private key
cert_file = os.path.join(root_ca_dir, "ca.pem")
key_file = os.path.join(root_ca_dir, "ca-key.pem")

# Read the certificate and private key from files
with open(cert_file, 'r') as cert:
    certificate_content = cert.read()

with open(key_file, 'r') as key:
    private_key_content = key.read()

url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/mtls_certificates"

data = {
    "ca": True,
    "certificates": certificate_content,
    "name": "example_ca_cert",
    "private_key": private_key_content
}

headers = {
    "Content-Type": "application/json",
    'X-Auth-Email': config.email,
    'X-Auth-Key': config.api_key
}

try:
    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200 and response.json().get('success'):
        print("Root CA uploaded successfully.")
        # Extract the "id" from the result
        root_ca_id = response.json()["result"]["id"]        
        print(f"Root CA ID: {root_ca_id}")
    else:
        print(f"Failed to upload certificate. Status code: {response.status_code}")
        print(f"Response content: {response.text}")

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")