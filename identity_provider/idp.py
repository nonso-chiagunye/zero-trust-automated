import requests
import sys
sys.path.append('..')
import config 

# Cloudflare base URL
url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/access/identity_providers"

data = {
    "config": {
        "client_id": config.okta_client_id, # Your OAuth Client ID
        "client_secret": config.okta_client_secret, # Your OAuth Client Secret
        "claims": ["email_verified", "preferred_username", "custom_claim_name"],
        "email_claim_name": "custom_claim_name", # The claim name for email in the id_token response
        "authorization_server_id": config.okta_authorization_server_id, # Your okta authorization server id
        "okta_account": "https://dev-abc123.oktapreview.com", # Your okta account url
    },
    # "id": config.okta_account_id,  # Unique ID for this IdP setup
    "name": "Okta",  # Name of the IdP
    "scim_config": {
        "enabled": True,  # Enable SCIM provisioning
        "group_member_deprovision": True,  # Remove users from groups upon de-provisioning
        "seat_deprovision": True,  # Remove access when de-provisioned
        "secret": config.okta_scim_secret,  # SCIM authentication secret
        "user_deprovision": True  # Automatically deactivate user accounts
    },
    "type": "okta"  # IdP type: 'okta', 'azure', etc.
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
        print("Identity provider configured successfully.")
        print("Response data:", response.json())
    else:
        print(f"Failed to configure the identity provider. Status code: {response.status_code}")
        print("Response content:", response.text)

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")


