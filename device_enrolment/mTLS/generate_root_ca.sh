#!/bin/bash

# Generate root certificate with Cloudflare PKI tool

# Create a new directory to store the Root CA
ROOT_CA_DIR="$HOME/cert-dir"
mkdir -p $ROOT_CA_DIR
cd $ROOT_CA_DIR
echo "Created directory $ROOT_CA_DIR for the Root CA."

# Create the Certificate Signing Request (CSR) and config files with the specified data

# Create ca-csr.json
cat > ca-csr.json <<EOL
{
  "CN": "Access Testing CA",
  "key": {
    "algo": "rsa",
    "size": 4096
  },
  "names": [
    {
      "C": "US",
      "L": "Austin",
      "O": "Access Testing",
      "OU": "TX",
      "ST": "Texas"
    }
  ]
}
EOL

echo "Created ca-csr.json file."

# Create ca-config.json
cat > ca-config.json <<EOL
{
  "signing": {
    "default": {
      "expiry": "8760h"
    },
    "profiles": {
      "server": {
        "usages": ["signing", "key encipherment", "server auth"],
        "expiry": "8760h"
      },
      "client": {
        "usages": ["signing", "key encipherment", "client auth"],
        "expiry": "8760h"
      }
    }
  }
}
EOL

echo "Created ca-config.json file."

# Generate the Root CA using the files
cfssl gencert -initca ca-csr.json | cfssljson -bare ca

if [ $? -eq 0 ]; then
    echo "Generated Root CA."
    # Check directory content to confirm successful output
    echo "Directory content:"
    ls -l    
else
    echo "Failed to agenerate root ca."
fi

# Expected output:
# ca-config.json ca-csr.json ca-key.pem ca.csr ca.pem
