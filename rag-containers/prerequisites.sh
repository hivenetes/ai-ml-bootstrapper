#!/bin/bash

# Navigate to the rag-containers directory 
cd ai-ml-bootstrapper/rag-containers

# Remove conflicting Docker packages
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done

# Update package list and install necessary packages
sudo apt-get update
sudo apt-get install -y ca-certificates curl

# Add Docker's official GPG key
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add Docker repository to Apt sources
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package list and install Docker packages
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Make the NVIDIA Container Toolkit installer script executable
chmod +x webapp/nvidia-container-toolkit-install.sh

# Run the NVIDIA Container Toolkit installer script
webapp/nvidia-container-toolkit-install.sh

# After installing Nvidia runtime toolkit, Set NVIDIA_RUNTIME envitonment variable to true
export NVIDIA_RUNTIME=true

# Install Nvidia Docker package 
sudo apt install -y nvidia-docker2

# Reload daemon and restart Docker
sudo systemctl daemon-reload
sudo systemctl restart docker

# Copy the secret.example.txt to secret.txt and update the DO_SPACES_KEY and DO_SPACES_SECRET values in secret.txt
cp store_service/secret.example.txt store_service/secret.txt

# Disable NVLink within the NVIDIA kernel module
echo "options nvidia NVreg_NvLinkDisable=1" | sudo tee /etc/modprobe.d/nvidia-disablenvlink.conf

# Update the RAM disk to apply the change
sudo update-initramfs -u

# Reboot the system to apply the changes
sudo reboot

# After reboot, Navigate to the rag-containers directory and execute run.sh script
cd ai-ml-bootstrapper/rag-containers
./run.sh
