#!/bin/bash

# HACS (Home Assistant Community Store) Installation Script
# Installiert HACS automatisch beim Start von Home Assistant

HACS_DIR="/config/custom_components/hacs"

# Check if HACS is already installed
if [ -d "$HACS_DIR" ]; then
    echo "HACS is already installed at $HACS_DIR"
    exit 0
fi

# Create custom_components directory if it doesn't exist
mkdir -p /config/custom_components

# Download HACS
echo "Downloading HACS..."
cd /config/custom_components

# Clone HACS repository
git clone https://github.com/hacs/integration.git hacs 2>/dev/null || {
    echo "Git clone failed, trying wget..."
    wget -q -O hacs.zip https://github.com/hacs/integration/archive/refs/heads/master.zip
    unzip -q hacs.zip
    rm hacs.zip
    mv integration-master hacs
}

echo "HACS installation completed at $HACS_DIR"

# Restart Home Assistant to load HACS (this will be handled by Home Assistant's normal reload)
exit 0
