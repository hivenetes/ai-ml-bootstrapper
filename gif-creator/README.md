# GIF Generator

The GIF Generator is a Python-based application that allows users to generate animated GIFs from text prompts. Users can enter a single prompt or multiple prompts separated by semicolons (`;`). The application uses the `diffusers` library to generate images based on the provided prompts and then combines these images into an animated GIF.

## Features

- Generate GIFs from single or multiple text prompts.
- User-friendly interface built with Gradio.
- Examples provided for easy usage.
- Uses State of the art Flux model for image generation

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
    --image 164081218 \
    --size gpu-h100x1-80gb \
    --ssh-keys <ssh::fingerprint>
```

### 2. Prepare the Environment

1. SSH into your GPU Droplet:
    ```bash
    ssh root@<gpu-droplet-ip>
    ```
2. Run the `./scripts/prerequisites.sh` script (this script ensures GPU availability for the application).
        - [Important]: This steps involves reboot of the VM
3. Clone the repository:
    ```bash
    git clone https://github.com/hivenetes/ai-ml-bootstrapper.git
    cd ai-ml-bootstrapper/gif-creator
    ```

### 3. Create a Virtual Environment

It is recommended to create a virtual environment to manage dependencies.

```python3 -m venv venv```

```source venv/bin/activate```  # On Windows, use `venv\Scripts\activate`


### 4. Install Dependencies

Install the required Python packages using `pip`.

```pip install -r requirements.txt```


## Usage

### Running the Application

To run the application, execute the following command:

```python3 gif_web.py```


This will launch the Gradio interface in your default web browser.

### Using the Interface

1. **Enter Prompt**: Enter a single prompt or multiple prompts separated by semicolons (`;`).
2. **Examples**: Click on the examples to auto-fill the prompt textbox.
3. **Generate GIF**: Click the "Generate GIF" button to generate and display the animated GIF.


## Troubleshooting

### Setting Up GPU

To use GPU for image generation, ensure you have CUDA installed and a compatible GPU.
