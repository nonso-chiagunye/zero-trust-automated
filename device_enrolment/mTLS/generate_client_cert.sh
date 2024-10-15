#!/bin/bash

# Generate client certificate with Cloudflare PKI tool

# Ensure you're in the Root CA directory
ROOT_CA_DIR="$HOME/cert-dir"
cd $ROOT_CA_DIR

# Create client-csr.json with the specified JSON content
cat > client-csr.json <<EOL
{
  "CN": "Your Name",
  "hosts": [""],
  "key": {
    "algo": "rsa",
    "size": 4096
  },
  "names": [
    {
      "C": "US",
      "L": "Austin",
      "O": "Access",
      "OU": "Access Admins",
      "ST": "Texas"
    }
  ]
}
EOL

echo "Created client-csr.json file."

# Generate the client certificate using the Cloudflare PKI toolkit
cfssl gencert -ca=ca.pem -ca-key=ca-key.pem -config=ca-config.json -profile=client client-csr.json | cfssljson -bare client

if [ $? -eq 0 ]; then
    echo "Generated client certificate."
    # Check directory content to confirm successful output
    echo "Directory content after client certificate generation:"
    ls -l    
else
    echo "Failed to agenerate client ca."
fi

# Expected new files:
# client.csr client-key.pem client.pem
