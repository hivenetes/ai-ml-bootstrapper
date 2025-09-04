# GIF Creator

This project is part of the [AI/ML Bootstrapper](https://github.com/hivenetes/ai-ml-bootstrapper) repository, designed to help users easily create GIFs from a single prompt. The GIF Creator module offers a simple way to generate animated GIFs using image generation, image to video generation and finally video to Gif images.

## Features

- Single prompt to create Gif
- **Dual Model Support**: Choose between Gemini 2.5 Flash Image (faster, cloud-based) or FLUX.1-dev (local GPU)
- Change Number of Inference steps, Guidance scale, Seed to adjust Image creation
- Automatic fallback between models for reliability

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
    --ssh-keys <ssh::fingerprint> # doctl compute ssh-key list to get fingerpritns
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

### Venv

```apt install python3.10-venv```

```python3 -m venv venv```

```source venv/bin/activate```  # On Windows, use `venv\Scripts\activate`

### uv

```
uv init
uv add -r requirements.txt
# use `uv sync` later to install locked versions
uv run gif_web.py
```


### 4. Install Dependencies

Install the required Python packages using `pip`.

```pip install -r requirements.txt```

### 5. API Keys Setup

#### Option 1: Google Gemini API (Recommended - Default Model)
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API key" to generate your API key
4. Create a `.env` file in the project directory:
   ```
   GEMINI_API_KEY=your_api_key_here
   MODEL_CHOICE=gemini
   ```
   
   The application will automatically load these variables from the `.env` file.
   
   Alternatively, you can set environment variables manually:
   ```bash
   export GEMINI_API_KEY="your_api_key_here"
   ```

#### Option 2: Huggingface (For FLUX.1-dev model)
Create a token in Hugginface and provide when below command is executed   
```huggingface-cli login```

or with uv `uv run huggingface-cli login`

### 6. Environment Variables

You can set the following environment variables to configure the application:

- `GEMINI_API_KEY`: Your Google AI API key for Gemini model (preferred)
- `GOOGLE_API_KEY`: Alternative name for Google AI API key (for compatibility)
- `MODEL_CHOICE`: Choose between `gemini` (default) or `flux`

Example `.env` file:
```
GEMINI_API_KEY=your_google_api_key_here
MODEL_CHOICE=gemini
```

## Quick Start

For immediate testing:
```bash
# Install dependencies
uv add -r requirements.txt  # or pip install -r requirements.txt

# Create .env file with your API key (optional, will fallback to FLUX if not provided)
echo "GEMINI_API_KEY=your_api_key_here" > .env
echo "MODEL_CHOICE=gemini" >> .env

# Run the application
uv run python gif_web.py    # or python gif_web.py
```

The application automatically loads settings from `.env` files - no manual environment variable setup needed!

## Usage

### Running the Application

To run the application, execute the following command:

```bash
uv run python gif_web.py
```
or
```bash
python3 gif_web.py
```

This will launch the Gradio interface in your default web browser at http://0.0.0.0:7860

### Using the Interface

1. **Enter Prompt**: Enter a prompt in textbox.
2. **Select Model**: Choose between "Gemini 2.5 Flash Image" (faster, requires API key) or "FLUX.1-dev" (local GPU).
3. **Examples**: Click on the examples to auto-fill the prompt textbox.
4. **Adjust Parameters**: Modify inference steps, guidance scale, and seed as needed.
5. **Generate GIF**: Click the "Generate GIF" button to generate and display the animated GIF.

### Model Comparison

| Feature | Gemini 2.5 Flash Image | FLUX.1-dev |
|---------|----------------------|-------------|
| Speed | ⚡ Faster | Slower |
| Cost | $0.039 per image | Free (uses local GPU) |
| Requirements | Internet + API Key | Local GPU + HuggingFace login |
| Quality | High | High |
| Fallback | Auto-fallback to FLUX if failed | None |


## Troubleshooting

### Setting Up GPU

To use GPU for image generation, ensure you have CUDA installed and a compatible GPU.

### Common Issues

#### Gemini API Issues

1. **"Gemini client not initialized" error**: 
   - Make sure you've set the `GEMINI_API_KEY` environment variable (or `GOOGLE_API_KEY` for compatibility)
   - Verify your API key is valid by testing it in Google AI Studio

2. **API quota exceeded (429 RESOURCE_EXHAUSTED)**: 
   - You've hit the free tier limits for Gemini API
   - Wait for quota to reset or upgrade your Google AI plan
   - The application will automatically fallback to FLUX.1-dev

3. **Internet connectivity issues**: 
   - Gemini requires internet connection to work
   - Use FLUX.1-dev model for offline operation

#### FLUX Model Issues

1. **"GatedRepoError" or "403 Client Error"**: 
   - FLUX.1-dev requires HuggingFace account access approval
   - Visit https://huggingface.co/black-forest-labs/FLUX.1-dev to request access
   - Then run: `huggingface-cli login` (or `uv run huggingface-cli login`)

2. **Model loading fails**:
   - Ensure you have sufficient GPU memory (FLUX requires significant VRAM)
   - Try restarting if models fail to load

### Model Fallback

The application includes automatic fallback:
- If Gemini fails (API issues, quota exceeded, etc.), it automatically switches to FLUX.1-dev
- No manual intervention needed - the error will be logged and the backup model will be used
