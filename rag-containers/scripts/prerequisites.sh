#!/bin/bash

# Manually install docker compose
DOCKER_CONFIG=${DOCKER_CONFIG:-$HOME/.docker}
mkdir -p $DOCKER_CONFIG/cli-plugins
curl -SL https://github.com/docker/compose/releases/download/v2.29.2/docker-compose-linux-x86_64 -o $DOCKER_CONFIG/cli-plugins/docker-compose
chmod +x $DOCKER_CONFIG/cli-plugins/docker-compose
docker compose version

# Install Nvidia Docker package
sudo apt install -y nvidia-docker2

# Reload daemon and restart Docker
sudo systemctl daemon-reload
sudo systemctl restart docker

# Disable NVLink within the NVIDIA kernel module
echo "options nvidia NVreg_NvLinkDisable=1" | sudo tee /etc/modprobe.d/nvidia-disablenvlink.conf

# Update the RAM disk to apply the change
sudo update-initramfs -u

# Reboot the system to apply the changes
sudo reboot