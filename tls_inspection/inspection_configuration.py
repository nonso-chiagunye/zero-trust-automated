# Enable TLS Inspection - Including anti-virus and deep packet inspection

import requests
import sys
sys.path.append('..')
import config

root_ca_id = "<YOUR ROOT CA ID>"  # Created earlier in mTLS

# Cloudflare API endpoint
url = f"https://api.cloudflare.com/client/v4/accounts/{config.account_id}/gateway/configuration"

# Parameters for updating the settings, including the root_ca_id, antivirus, dpi, sandboxing
data = {
    "settings": {
        "activity_log": {
            "enabled": True
        },
        "antivirus": {
            "enabled_download_phase": True,
            "enabled_upload_phase": True,
            "fail_closed": True,
            "notification_settings": {
                "enabled": True,
                "msg": "Something went wrong, please try again or contact support",
                "support_url": "https://support.company.com/"
            }
        },
        "block_page": {
            "background_color": "string",
            "enabled": True,
            "footer_text": "--footer--",
            "header_text": "--header--",
            "logo_path": "https://logos.com/a.png",
            "mailto_address": "admin@mycompany.com",
            "mailto_subject": "Blocked Malicious Traffic",
            "name": "Company Name",
            "suppress_footer": False
        },
        "body_scanning": {
            "inspection_mode": "deep"
        },
        "browser_isolation": {
            "non_identity_enabled": True,
            "url_browser_isolation_enabled": True
        },
        "certificate": {
            "id": root_ca_id  # Using the root_ca_id variable here
        },
        "extended_email_matching": {
            "enabled": True
        },
        "fips": {
            "tls": True
        },
        "protocol_detection": {
            "enabled": True
        },
        "sandbox": {
            "enabled": True,
            "fallback_action": "allow"
        },
        "tls_decrypt": {
            "enabled": True
        }
    }
}

# Headers
headers = {
    "Content-Type": "application/json",
    'X-Auth-Email': config.email,
    'X-Auth-Key': config.api_key
}

try:
    # Make the PATCH request to update the settings
    response = requests.patch(url, json=data, headers=headers)

    # Check if the request was successful
    if response.status_code == 200 and response.json().get('success'):
        print("Configuration updated successfully.")        
    else:
        print(f"Failed to update configuration. Status code: {response.status_code}")
        print(response.text)

except requests.exceptions.RequestException as e:
    # Handle any request-related errors 
    print(f"An error occurred: {e}")

