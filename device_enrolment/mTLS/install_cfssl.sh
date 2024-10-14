#!/bin/bash

# Download and install Cloudflare open source PKI tool

# Check if go is installed
check_go_installed() {
    if command -v go >/dev/null 2>&1; then
        echo "Go is installed."
        return 0
    else
        echo "Go is not installed. Installing Go..."
        install_go
        return 1
    fi
}

# Install go if it is not installed
install_go() {
    wget https://go.dev/dl/go1.23.2.linux-amd64.tar.gz
    sudo tar -C /usr/local -xzf go1.23.2.linux-amd64.tar.gz
    export PATH=$PATH:/usr/local/go/bin
    echo "Go has been installed."
}

# Check go version, and install Cloudflare cfssl tool according to go version
check_go_version() {
    go_version=$(go version | awk '{print $3}' | sed 's/go//g')
    echo "Go version is $go_version"
    if [[ $(echo "$go_version <= 1.18" | bc -l) -eq 1 ]]; then
        echo "Go version is 1.18 or below. Installing cfssl using go get..."
        go get github.com/cloudflare/cfssl/cmd/...

        if [ $? -eq 0 ]; then
            echo "cfssl tool installed successfully."  
        else
            echo "Failed to install cfssl tool."
        fi

        
    else
        echo "Go version is above 1.18. Installing cfssl using go install..."
        go install github.com/cloudflare/cfssl/cmd/...@latest

        if [ $? -eq 0 ]; then
            echo "cfssl tool installed successfully."
        else
            echo "Failed to install cfssl tool."
        fi
    fi
}

# Execute go install check
check_go_installed
# Execute go version check and install cfssl tool 
check_go_version
