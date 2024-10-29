
# Text to Speech with NIMs on GPU Droplets

This guide provides steps for setting up an Text to Speech (tts) environment using NVIDIA NIMs on DigitalOcean GPU droplets, including client setup instructions and a demonstration video.

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
   export NGC_API_KEY=<your_ngc_api_key>
   ```

3. **Run the TTS Container**:

   Pull and run `nvidia/fastpitch-hifigan-tts` NIM
   Deploy the TTS container using the command below. Replace `<ngc_api_key>` with your NGC API Key:

   > **Note**: This cache directory is to where models are downloaded inside the container. If this volume is not mounted, the container does a fresh download of the model every time the container starts.

   ```bash
   mkdir ~/nim-cache
   export NIM_CACHE_PATH=~/nim-cache
   sudo chmod -R 777 $NIM_CACHE_PATH
   ```

   Let's spin up the TTS container

   ```bash
   export CONTAINER_NAME=fastpitch-hifigan-tts
   docker run -it --rm --name=$CONTAINER_NAME \
     --runtime=nvidia \
     --gpus '"device=0"' \
     --shm-size=8GB \
     -e NGC_API_KEY=$NGC_API_KEY \
     -e NIM_MANIFEST_PROFILE=3c8ee3ee-477f-11ef-aa12-1b4e6406fad5 \
     -e NIM_HTTP_API_PORT=9001 \
     -e NIM_GRPC_API_PORT=50052 \
     -v $NIM_CACHE_PATH:/opt/nim/.cache \
     -p 9001:9001 \
     -p 50052:50052 \
     nvcr.io/nim/nvidia/fastpitch-hifigan-tts:1.0.0
   ```

4. **Access the ASR Service**:

   Once the container is up, access the ASR service at the public IP of your GPU Droplet on the following ports:
   - HTTP: `9001`
   - gRPC: `50052`

## Transription RIVA Client Setup

Install the following dependencies on your client machine:

```bash
pip3 install nvidia-riva-client
pip3 install PyAudio
```

### Running the Transcription Client

Use the following command to transcribe audio from your microphone:

```bash
python3 clients/talk.py --server <public-ip>:50052 \
  --text \
  "Now available for every DigitalOcean user,
  GPU Droplets are powered by NVIDIA H100 GPUs, which are one of the most powerful computers accessible today,
  and feature 640 Tensor Cores and 128 Ray Tracing Cores, facilitating high-speed data processing. 
  GPU Droplets offer on-demand access to these machines, enabling developers, startups, and innovators to train AI models, 
  process large datasets, and handle complex neural networks with ease." \
  --language-code en-US \
  --output-device 1 --stream
```

Replace `<public-ip>` with the public IP of your GPU Droplet.

## Additional Resources

For more details, check out the [NVIDIA NGC TTS-HIFIGAN Documentation](https://build.nvidia.com/nvidia/fastpitch-hifigan-tts/docker).
