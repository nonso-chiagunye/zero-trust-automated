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
- Generate root and client certificate. Upload root cert to cloudflare, and add client cert to system keychain
- [Step 1:](device_enrolment/mTLS/install_cfssl.sh) Download Cloudflare ssl tool (cfssl), build and install on your linux machine
- [Step 2:](device_enrolment/mTLS/generate_root_ca.sh) Generate root ca and key pair with cfssl
- [Step 3:](device_enrolment/mTLS/generate_client_cert.sh) Generate client ca with cfssl
- [Step 4:](device_enrolment/mTLS/upload_root_cert.py) Upload the root cert to Cloudflare
- [Step 5:](device_enrolment/mTLS/client_cert/) Add client cert to system keychain with bash (Linux) or PowerShell (Windows)

## [Device Posture Assessment](device_posture)

## [Gateway Rules](gateway_rules)

## [Data Loss Prevention](data_loss_prevention)

## [TLS Inspection](tls_inspection)

## [Threat Intelligence](threat_intel)
