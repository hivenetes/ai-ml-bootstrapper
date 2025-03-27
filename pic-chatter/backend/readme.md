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
   git clone https://github.com/yourusername/pic-chatter-backend.git
   cd pic-chatter-backend
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

   - **API Key**: Use 1 Click Models in GPU Droplets to deploy a [LLlama Vision Instruct model](https://marketplace.digitalocean.com/apps/meta-llama-llama-3-1-70b-instruct-8x) and replace the IP address and Bearer token in .env file.
   - Update spaces endpoint URL in .env file


## Usage

1. **Run the application**:

   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API**:

   - **Root Endpoint**: `GET /` - Returns a welcome message.
   - **Image Description Endpoint**: `GET /get_image_description` - Returns a description of the specified image.

