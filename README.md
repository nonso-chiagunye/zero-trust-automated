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

## [Device Posture Assessment](device_posture)

## [Gateway Rules](gateway_rules)

## [Data Loss Prevention](data_loss_prevention)

## [TLS Inspection](tls_inspection)

## [Threat Intelligence](threat_intel)
