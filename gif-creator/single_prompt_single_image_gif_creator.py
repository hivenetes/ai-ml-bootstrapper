import random
import gradio as gr
import numpy as np
import torch
from diffusers import FluxPipeline
from diffusers import DiffusionPipeline
from PIL import Image
from diffusers.utils import export_to_gif

device = "cuda" if torch.cuda.is_available() else "cpu"
HEIGHT = 256
WIDTH = 1024
MAX_SEED = np.iinfo(np.int32).max

def split_image(input_image, num_splits=4):
    # Create a list to store the output images
    output_images = []

    # Split the image into four 256x256 sections
    for i in range(num_splits):
        left = i * 256
        right = (i + 1) * 256
        box = (left, 0, right, 256)
        output_images.append(input_image.crop(box))

    return output_images

def predict(model_choice, prompt, num_inference_steps, guidance_scale, seed, progress=gr.Progress(track_tqdm=True)):
#def predict(model_choice, prompt, seed=42, randomize_seed=False, guidance_scale=5.0, num_inference_steps=28, progress=gr.Progress(track_tqdm=True)):
    if(model_choice == "Flux"):
        pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16).to(device)
        pipe.enable_model_cpu_offload()
    else:
        pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
        pipe.to(device)
    
    prompt_template = f"""
    A  side by side 4 frame image showing consecutive stills from a looped gif moving from left to right.
    The gif is of {prompt}.
    """

    seed = random.randint(0, MAX_SEED)

    image = pipe(
        prompt=prompt_template,
        guidance_scale=guidance_scale,
        num_inference_steps=num_inference_steps,
        num_images_per_prompt=1,
        generator=torch.Generator(device).manual_seed(seed),
        height=HEIGHT,
        width=WIDTH
    ).images[0]

    return export_to_gif(split_image(image, 4), "flux.gif", fps=4)
