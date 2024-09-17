#!/bin/bash

# Disable NVLink within the NVIDIA kernel module
echo "Disabling NVLink..."
echo "options nvidia NVreg_NvLinkDisable=1" | sudo tee /etc/modprobe.d/nvidia-disablenvlink.conf || error_exit "Failed to disable NVLink."

# Update the RAM disk to apply the change
echo "Updating initramfs..."
sudo update-initramfs -u || error_exit "Failed to update initramfs."

# Reboot the system to apply the changes
echo "Rebooting the system to apply changes..."
sudo reboot