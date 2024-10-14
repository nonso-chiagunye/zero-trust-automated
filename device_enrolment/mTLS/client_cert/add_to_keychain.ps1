# Add the client certificate to system keychain (Windows)

# Directory where the client certificate is located
$certDir = "$HOME\cert-dir"
$certFile = Join-Path $certDir "client.pem"

# Check if the client.pem file exists
if (-Not (Test-Path $certFile)) {
    Write-Host "Certificate file not found: $certFile"
    exit
}

# Convert the PEM certificate to a PFX format if needed
$pfxFile = Join-Path $certDir "client.pfx"

# Import the PEM client certificate (no private key needed in this case)
try {
    Write-Host "Importing client certificate into the Personal store..."
    $cert = Get-PfxCertificate -FilePath $certFile
    Import-Certificate -FilePath $certFile -CertStoreLocation Cert:\LocalMachine\My
    Write-Host "Client certificate added successfully to the system keychain."
} catch {
    Write-Host "Error: Unable to import the certificate to the system keychain."
}
