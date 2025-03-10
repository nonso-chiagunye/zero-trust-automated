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

## [Create Tunnel](tunnels)

- Create tunnel to connect private networks and applications to Cloudflare
- This project uses Cloudflared tunnel type (You can use WARP Connector tunnel type)
- First create a [tunnel](tunnels/tunnel.py)
- Then configure [routes](tunnels/tunnel_routes.py) to private networks

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

## [Create Device Profiles](warp_settings)

- Device profile settings control what is allowed on end-user device side (unlike gateway policies that control what is allowed at the Cloudflare gateway side)
- Best practice: make the 'Deafult Profile' as strict as possible, then create individual profiles to make exceptions for users as required
- Create a new [device profile](warp_settings/custom_device_profile.py)
- Create [local domain fallback](warp_settings/local_domail_fallback.py) to allow domain resolution by a local DNS server
- Create [split tunnel](warp_settings/split_tunnel_exclude.py) to exclude IPs or URLs that shouldn't be routed through Cloudflare global network

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

- TLS Inspection analysis the body of traffic (req.body) for threats
- It involves decrypting the traffic, analyzing it, encrypting back before forwarding to destination
- Included are antivirus, sandboxing, deep packet inspection, etc
- It requires a root certificate for the tls termination. [This project](tls_inspection/inspection_configuration.py) used the root certificate uploaded above (in mTLS)
- I also included a list of IPs that should be excluded from inspection (like Pentest IPs)

## [Threat Intelligence](threat_intel)

- Cloudflare allows creation of custom indicators where you can upload threat feeds. They must be in stix 2 format
- Steps involved creating this threat intel;
- [Step 1:](threat_intel/custom_indicator.py) Create custom indicator feed instance
- [Step 2:](threat_intel/create_rule.py) Create gateway rule that matches traffic based on the indicator feed
- [Step 3:](threat_intel/fetch_upload_feeds.py) Fetch threat intel feeds from threat intel providers. You can combine multiple feeds from multiple providers (here I fetched IP drops from spamhaus)
- [Step 4:](threat_intel/fetch_upload_feeds.py) Convert the threat feeds to .stix2 format and upload to the custom indicator feed instance created earlier
- [Step 5:](threat_intel/schedules) Schedule a cron (bash/Linux) or task (PowerShell/Windows) to run the function daily, to fetch new threat feeds, convert to .stix2 and upload to Cloudflare.
