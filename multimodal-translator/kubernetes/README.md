# Kubernetes Setup

## Prerequisites

- kubectl
- NVIDIA GPU Operator
- DigitalOcean account

## Setup Instructions

### 1. Create NFS Server Droplet

1. Create a new Droplet in DigitalOcean using doctl:

   ```bash
   doctl compute droplet create nfs-server \
     --image ubuntu-22-04-x64 \
     --size s-2vcpu-2gb \
     --region <your-region>
   ```

   Make sure to:
   - Use Ubuntu 22.04 LTS image
   - Select at least Basic plan (2GB RAM)
   - Choose same datacenter region as your K8s cluster

2. SSH into the Droplet and set up NFS server:

   ```bash
   # Install NFS server
   sudo apt update
   sudo apt install nfs-kernel-server -y

   # Create export directory
   sudo mkdir -p /mnt/nfs_share
   sudo chown nobody:nogroup /mnt/nfs_share
   sudo chmod 777 /mnt/nfs_share

   # Configure exports
   echo "/mnt/nfs_share *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports
   sudo exportfs -a
   sudo systemctl restart nfs-kernel-server
   ```

3. Note down the Droplet's IP address - you'll need it for the next step.

### 2. Set up NFS StorageClass in Kubernetes

1. Install the NFS client provisioner:

   ```bash
   helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/
   helm repo update
   ```

2. Create a values.yaml file:

   ```yaml
   nfs:
     server: <YOUR-NFS-SERVER-IP>
     path: /mnt/nfs_share
   storageClass:
     name: nfs
     defaultClass: false
   ```

3. Install the helm chart:

   ```bash
   helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner -f values.yaml
   ```

## Manifest Documentation

The `manifest.yaml` file defines the following resources:

### Namespace

- Creates `nim-apps` namespace for all resources

### Persistent Volume Claims

Creates four PVCs for model caches and NVS storage:

- `parakeet-cache-pvc`: 100GB for Parakeet model cache
- `parakeet-nvs-pvc`: 100GB for Parakeet NVS storage
- `megatron-cache-pvc`: 100GB for Megatron model cache
- `megatron-nvs-pvc`: 100GB for Megatron NVS storage

### Parakeet CTC Deployment

Deploys the Parakeet ASR (Automatic Speech Recognition) model:

- Image: `nvcr.io/nim/nvidia/parakeet-ctc-1.1b-asr:1.0.0`
- GPU requirements: Uses NVIDIA H100 GPUs
- Ports:
  - HTTP API: 9000
  - gRPC API: 50051
- Volume mounts for cache and NVS storage
- Environment configuration for NGC API and model profile

### Megatron Deployment

Deploys the Megatron Neural Machine Translation model:

- Image: `nvcr.io/nim/nvidia/megatron-1b-nmt:1.0.0`
- GPU requirements: Uses NVIDIA GPUs
- Ports:
  - HTTP API: 9000 (exposed as 9001)
  - gRPC API: 50051 (exposed as 50052)
- Volume mounts for cache and NVS storage
- Environment configuration for NGC API and model profile

### Services

Creates LoadBalancer services for both deployments:

- `parakeet-service`: Exposes Parakeet ASR endpoints
  - HTTP: 9000
  - gRPC: 50051
- `megatron-service`: Exposes Megatron NMT endpoints
  - HTTP: 9001 → 9000
  - gRPC: 50052 → 50051

## Important Notes

1. Replace `your-api-key` in the manifest with your actual NGC API key
2. Ensure your Kubernetes cluster has NVIDIA GPUs available
3. The manifest uses DigitalOcean-specific annotations for LoadBalancer configuration
4. Both services are exposed via LoadBalancer - ensure proper security measures are in place
