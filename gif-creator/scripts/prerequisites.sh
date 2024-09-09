#!/bin/bash

# Disable NVLink within the NVIDIA kernel module
echo "options nvidia NVreg_NvLinkDisable=1" | sudo tee /etc/modprobe.d/nvidia-disablenvlink.conf

# Update the RAM disk to apply the change
sudo update-initramfs -u

# Reboot the system to apply the changes
sudo reboot