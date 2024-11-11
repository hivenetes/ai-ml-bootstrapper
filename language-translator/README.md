
# Language Translator NIMs on GPU Droplets

This guide provides steps for setting up an Language Translator environment using NVIDIA NIMs on DigitalOcean GPU droplets, including client setup instructions.

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
   export NGC_CLI_API_KEY=<your_ngc_api_key>
   ```

3. **Run the TTS Container**:

   Pull and run `nvidia/megatron-1b-nmt` NIM
   Deploy the TTS container using the command below. Replace `<ngc_api_key>` with your NGC API Key:

   > **Note**: This cache directory is to where models are downloaded inside the container. If this volume is not mounted, the container does a fresh download of the model every time the container starts.

   ```bash
   docker login nvcr.io
   Username: $oauthtoken
   Password: <PASTE_API_KEY_HERE>
   ```

   Let's spin up the Language Translator container

   ```bash
   mkdir ~/nim-cache
   export NIM_CACHE_PATH=~/nim-cache
   sudo chmod -R 777 $NIM_CACHE_PATH

   export CONTAINER_NAME=megatron-1b-nmt
   docker run -it --rm --name=$CONTAINER_NAME \
     --runtime=nvidia \
     --gpus '"device=0"' \
     --shm-size=8GB \
     -e NGC_CLI_API_KEY=$NGC_CLI_API_KEY \
     -e NIM_MANIFEST_PROFILE=89e2a0b4-477e-11ef-b226-cf5f41e3c684 \
     -e NIM_HTTP_API_PORT=9000 \
     -e NIM_GRPC_API_PORT=50051 \
     -p 9000:9000 \
     -p 50051:50051 \
     nvcr.io/nim/nvidia/megatron-1b-nmt:1.0.0
   ```

4. **Access the ASR Service**:

   Once the container is up, access the ASR service at the public IP of your GPU Droplet on the following ports:
   - HTTP: `9000`
   - gRPC: `50051`

## Transription RIVA Client Setup

Install the following dependencies on your client machine:

```bash
pip3 install nvidia-riva-client
```

### Running the Transcription Client

Use the following command to transcribe audio from your microphone:

```bash
python3 client.py --server <public-ip-address>:50051 --text "Have you tried DigitalOcean GPU Dropelts yet?" --source-language-code en --target-language-code de
```

Replace `<public-ip>` with the public IP of your GPU Droplet.

Example output:

```bash
   Hast du DigitalOcean GPU Dropelts schon ausprobiert?
```

## Additional Resources

For more details, check out the [NVIDIA NGC MEGATRON-1B-NMT Documentation](https://build.nvidia.com/nvidia/megatron-1b-nmt/docker).
