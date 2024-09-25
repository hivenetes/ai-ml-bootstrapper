# GIF Creator

This project is part of the [AI/ML Bootstrapper](https://github.com/hivenetes/ai-ml-bootstrapper) repository, designed to help users easily create GIFs from a single prompt. The GIF Creator module offers a simple way to generate animated GIFs using image generation, image to video generation and finally video to Gif images.

## Features

- Single prompt to create Gif
- Change Number of Inference steps, Guidance scale, Seed to adjust Image creation

## Installation

### Prerequisites

Before starting, ensure you have the following:

- A [DigitalOcean account](https://cloud.digitalocean.com/registrations/new).
- `doctl` CLI installed. Follow the [installation guide](https://docs.digitalocean.com/reference/doctl/how-to/install/).

> **Note**: These steps are platform-agnostic and should work on any OS with minor adjustments.

## Set up Infrastructure

### 1. Spin Up a GPU Droplet

Use the following command to create a GPU droplet in the `TOR1` datacenter, equipped with a single H100 GPU:

```bash
doctl compute droplet create <droplet-name> \
    --region tor1 \
    --image gpu-h100x1-base \
    --size gpu-h100x1-80gb \
    --ssh-keys <ssh::fingerprint>
```

### 2. Prepare the Environment

1. SSH into your GPU Droplet:
    ```bash
    ssh root@<gpu-droplet-ip>
    ```
2. Clone the repository:
    ```bash
    git clone https://github.com/hivenetes/ai-ml-bootstrapper.git
    cd ai-ml-bootstrapper/gif-creator
    ```

### 3. Create a Virtual Environment

It is recommended to create a virtual environment to manage dependencies.

```apt install python3.10-venv```

```python3 -m venv venv```

```source venv/bin/activate```  # On Windows, use `venv\Scripts\activate`


### 4. Install Dependencies

Install the required Python packages using `pip`.

```pip install -r requirements.txt```

### 5. Huggingface Cli Login

Create a token in Hugginface and provide when below command is executed   
```huggingface-cli login```

## Usage

### Running the Application

To run the application, execute the following command:

```python3 gif_web.py```


This will launch the Gradio interface in your default web browser.

### Using the Interface

1. **Enter Prompt**: Enter a prompt in textbox.
2. **Examples**: Click on the examples to auto-fill the prompt textbox.
3. **Generate GIF**: Click the "Generate GIF" button to generate and display the animated GIF.


## Troubleshooting

### Setting Up GPU

To use GPU for image generation, ensure you have CUDA installed and a compatible GPU.
