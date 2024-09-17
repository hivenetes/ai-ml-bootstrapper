#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Function to display an error message and exit
error_exit() {
    echo "Error: $1"
    exit 1
}

# Install Python3 venv if not installed
echo "Checking for Python3 venv..."
if ! dpkg -l | grep -q python3-venv; then
    echo "Installing python3-venv..."
    sudo apt update
    sudo apt install -y python3.10-venv || error_exit "Failed to install python3.10-venv."
else
    echo "python3-venv already installed."
fi

# Create and activate Python virtual environment
echo "Creating virtual environment..."
python3 -m venv venv || error_exit "Failed to create virtual environment."
source venv/bin/activate || error_exit "Failed to activate virtual environment."

# Install Python dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt || error_exit "Failed to install dependencies."

# Disable NVLink within the NVIDIA kernel module
echo "Disabling NVLink..."
echo "options nvidia NVreg_NvLinkDisable=1" | sudo tee /etc/modprobe.d/nvidia-disablenvlink.conf || error_exit "Failed to disable NVLink."

# Update the RAM disk to apply the change
echo "Updating initramfs..."
sudo update-initramfs -u || error_exit "Failed to update initramfs."

# Reboot the system to apply the changes
echo "Rebooting the system to apply changes..."
sudo reboot