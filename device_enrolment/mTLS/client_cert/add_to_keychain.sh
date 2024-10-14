#!/bin/bash

# Add the client certificate to system keychain (Linux)

# Directory where the client certificate is located
CERT_DIR="$HOME/cert-dir"
CERT_FILE="$CERT_DIR/client.pem"

# Check if the client.pem file exists
if [ ! -f "$CERT_FILE" ]; then
    echo "Certificate file not found: $CERT_FILE"
    exit 1
fi

# Ensure the certutil command is available (part of nss-tools package)
if ! command -v certutil &> /dev/null; then
    echo "certutil not found. Please install nss-tools."
    echo "On Debian-based systems: sudo apt install libnss3-tools"
    echo "On RedHat-based systems: sudo yum install nss-tools"
    exit 1
fi

# Add the client certificate to the system keychain
echo "Adding client certificate to the system keychain..."

# Create a database directory for the certificates if it doesn't exist
DB_DIR="/etc/pki/nssdb"
sudo mkdir -p $DB_DIR
sudo certutil -d sql:$DB_DIR -A -t "CT,C,C" -n "client_cert" -i "$CERT_FILE"

if [ $? -eq 0 ]; then
    echo "Client certificate added successfully to the system keychain."
else
    echo "Failed to add the client certificate to the system keychain."
fi
