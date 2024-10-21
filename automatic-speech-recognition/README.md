
# Automatic Speech Recognition with NIMs on GPU Droplets

This guide provides steps for setting up an Automatic Speech Recognition (ASR) environment using NVIDIA NIMs on DigitalOcean GPU droplets, including client setup instructions and a demonstration video.

## Prerequisites

Ensure you have the following:

- **DigitalOcean CLI - [doctl](https://docs.digitalocean.com/reference/doctl/how-to/install/)**
- **NGC API Key**: Generate one from [NVIDIA NGC](https://org.ngc.nvidia.com/setup/api-key)

## NVIDIA Triton/RIVA Server Setup

1. **Create a GPU Droplet**:

   Use `doctl` to spin up a GPU Droplet, replacing `<region>` and `<ssh-key-fingerprint>` with appropriate values:

   ```bash
   doctl compute droplet create ab-ai-ctk --region <tor1/ams3> --image gpu-h100x1-base --size gpu-h100x1-80gb --ssh-keys <ssh-key-fingerprint>
   ```

2. **Set Environment Variables**:

   Set up the required environment variables:

   ```bash
   export NGC_API_KEY=<ngc_api_key>
   ```

3. **Run the ASR Container**:

   Pull and run `nvidia/parakeet-ctc-1_1b-asr` NIM
   Deploy the ASR container using the command below. Replace `<ngc_api_key>` with your NGC API Key:

   > **Note**: This cache directory is to where models are downloaded inside the container. If this volume is not mounted, the container does a fresh download of the model every time the container starts.

   ```bash
   mkdir ~/nim-cache
   export NIM_CACHE_PATH=~/nim-cache
   sudo chmod -R 777 $NIM_CACHE_PATH
   ```

   Let's spin up the ASR container

   ```bash
   export CONTAINER_NAME=parakeet-ctc-1.1b-asr
   docker run -it --rm --name=$CONTAINER_NAME \
      --runtime=nvidia \
      --gpus '"device=0"' \
      --shm-size=8GB \
      -e NGC_API_KEY=$NGC_API_KEY \
      -e NIM_MANIFEST_PROFILE=9136dd64-4777-11ef-9f27-37cfd56fa6ee \
      -e NIM_HTTP_API_PORT=9000 \
      -e NIM_GRPC_API_PORT=50051 \
      -v $NIM_CACHE_PATH:/opt/nim/.cache \
      -p 9000:9000 \
      -p 50051:50051 \
      nvcr.io/nim/nvidia/parakeet-ctc-1.1b-asr:1.0.0
   ```

4. **Access the ASR Service**:

   Once the container is up, access the ASR service at the public IP of your GPU Droplet on the following ports:
   - HTTP: `9000`
   - gRPC: `50051`

## Transription RIVA Client Setup

Install the following dependencies on your client machine:

```bash
pip3 install nvidia-riva-client
pip3 install PyAudio
```

### Running the Transcription Client

Use the following command to transcribe audio from your microphone:

```bash
python3 client.py --server <public-ip>:9000 --input-device 0 --language-code en-US
```

Replace `<public-ip>` with the public IP of your GPU Droplet.

## Demo in Action

[![Watch the video](https://img.youtube.com/vi/FKZ5loixyK8/0.jpg)](https://youtu.be/FKZ5loixyK8)

## Additional Resources

For more details, check out the [NVIDIA NGC Parakeet Documentation](https://build.nvidia.com/nvidia/parakeet-ctc-1_1b-asr/docker).
