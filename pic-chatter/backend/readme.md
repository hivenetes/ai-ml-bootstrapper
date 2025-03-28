# PicChatter Backend

Welcome to the PicChatter Backend, a FastAPI application that provides image description services.

## Features

- **Image Description**: Retrieve detailed descriptions of images using a specified API.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Requests

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/hivenetes/ai-ml-bootstrapper.git
   cd pic-chatter/backend
   ```

2. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. Configuration

   - **Model Setup**: Deploy a Llama Vision Instruct model using DigitalOcean's 1-Click GPU Droplets
     - Visit the [Llama 3 70B Instruct model](https://marketplace.digitalocean.com/apps/meta-llama-llama-3-1-70b-instruct-8x) on DigitalOcean Marketplace
     - Deploy the model to a GPU Droplet
     - After deployment, access the Droplet and retrieve the bearer token
     - Update the `.env` file with:
       - The GPU Droplet's IP address
       - The bearer token
     - These credentials will be used to authenticate and connect to the Llama model for image inference requests

   - **Spaces Setup**: Configure DigitalOcean Spaces for image storage
     - Access the DigitalOcean Cloud Console
     - Retrieve the Spaces endpoint URL created during front end application configuration
     - Update the Spaces endpoint URL to your `.env` file

## Usage

1. **Run the application**:

   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API**:

   - **Root Endpoint**: `GET /` - Returns a welcome message.
   - **Image Description Endpoint**: `GET /get_image_description` - Returns a description of the specified image.

