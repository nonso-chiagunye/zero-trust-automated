<h1 align="center">Zero Trust with Cloudflare</h1>

---

# Deployment Steps

---

## [Create Zero Trust Organization](organization)

- Creates a zero trust organization
- Chooses a unique team name for device enrolment through warp
- Users will need to specify the team name in order to join your zero trust network
- Sets general rules about authentication and sessions

## [Identity Provider Integration](identity_provider)

- Authenticates users and devices into the zero trust network
- This project used Okta as idp.
- You can select from a list of [supported idps](https://developers.cloudflare.com/api/operations/access-identity-providers-add-an-access-identity-provider)

## [Device Enrolment Policy](device_enrolment)

- Sets the policy conditions for allowing a device enrol into your zero trust network
- Only controls device enrolment, not access to your private networks and applications

➡️ **Whitelist Devices with Mutual TLS ([mTLS](device_enrolment/mTLS))**

- Use mutual TLS if you want to allow only specific devices (like company issued devices) to enroll in your zero trust network
- Generate root and client certificate. Upload root cert to cloudflare, and add client cert to client system keychain with these steps;
- [Step 1:](device_enrolment/mTLS/install_cfssl.sh) Download Cloudflare ssl tool (cfssl), build and install on your linux machine
- [Step 2:](device_enrolment/mTLS/generate_root_ca.sh) Generate root ca and key pair with cfssl
- [Step 3:](device_enrolment/mTLS/generate_client_cert.sh) Generate client ca with cfssl
- [Step 4:](device_enrolment/mTLS/upload_root_cert.py) Upload the root cert to Cloudflare
- [Step 5:](device_enrolment/mTLS/client_cert/) Add client cert to system keychain with bash (Linux) or PowerShell (Windows)

## [Device Posture Assessment](device_posture)

- An integral part of zero trust architecture
- You can use Cloudflare Warp or 3rd party endpoint solution to assess device posture
- I used Crowdstrike. There are [other supported endpoint solution](https://developers.cloudflare.com/api/operations/device-posture-integrations-create-device-posture-integration). Steps involved;
- Step 1: Create new API client on CrowdStrike, to get client id, client secret and base url
- [Step 2:](device_posture/crowdstrike_auth_token.sh) Get an auth token from CrowdStrike
- [Step 3:](device_posture/device_posture_integration.py) Integrate CrowdStrike as device posture provider
- [Step 4:](device_posture/posture_rule.py) Create device posture rules, specifying parameters that must be met before a device is allowed access
- [Step 5:](device_posture/gateway_rule.py) Create gateway rule based on the device posture rule. You can create a blanket, high-priority (low precedence) rule covering your entire network, or add device_posture.checks.passed as a condition in other gateway rules.

## [Gateway Rules](gateway_rules)

- [DNS](gateway_rules/dns_rule.py) rule creates dns security policy
- [Http](gateway_rules/http_rule.py) rule creates http security policy
- [l4](gateway_rules/network_rule.py) rule creats network security policy

## [Data Loss Prevention](data_loss_prevention)

- Cloudflare has predefined dlp profiles for various use cases (Finance, Health, Credentials and Secrets, etc)
- You can also create custom dlp profiles according to your sensitive data structure.
- This project combines predefined and custom profile entries into one [profile](data_loss_prevention/dlp_profile.py). The steps below;
- Step 1: A function to make a GET request to multiple predefined profiles, and extract the necessary entries.
- Step 2: Use regex to create a custom dlp matching pattern (according to target data structure)
- Step 3: Combine the predefined and custom entries in one custom dlp profile
- Step 4: Use the custom profile to create a [gateway rule](data_loss_prevention/dlp_gateway_rule.py) that blocks traffic matching the dlp profile.

## [TLS Inspection](tls_inspection)

## [Threat Intelligence](threat_intel)
