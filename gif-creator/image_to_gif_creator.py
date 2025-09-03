import torch
import numpy as np
import gradio as gr
import os
from glob import glob
from pathlib import Path
from typing import Optional
import random
from PIL import Image
from moviepy import VideoFileClip
from diffusers import DiffusionPipeline
from diffusers.utils import export_to_video
from diffusers import FluxPipeline

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-video-diffusion-img2vid-xt")
pipe.to(device)

max_64_bit_int = 2**63 - 1

def generateGif(prompt, num_inference_steps, guidance_scale, seed):
    text_to_img_pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16)
    text_to_img_pipe.enable_model_cpu_offload()

    generated_image = text_to_img_pipe(
        prompt=prompt,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        generator=torch.Generator(device).manual_seed(seed)
    ).images[0]

    os.makedirs("outputs", exist_ok=True)

    generated_image.save("outputs/generated_image.png")
    resized_image = resize_image(generated_image)
    video_path = generateVideo(resized_image)

    gif_path = convertVideoToGif()
    return gif_path

def generateVideo(
    image: Image,
    seed: Optional[int] = 42,
    randomize_seed: bool = True,
    motion_bucket_id: int = 127,
    fps_id: int = 6,
    version: str = "svd_xt",
    cond_aug: float = 0.02,
    decoding_t: int = 3,  # Number of frames decoded at a time! This eats most VRAM. Reduce if necessary.
    device: str = "cuda",
    output_folder: str = "outputs",
    progress=gr.Progress(track_tqdm=True)
):
    if image.mode == "RGBA":
        image = image.convert("RGB")
        
    if(randomize_seed):
        seed = random.randint(0, max_64_bit_int)
    generator = torch.manual_seed(seed)
    
    os.makedirs(output_folder, exist_ok=True)
    video_path = os.path.join(output_folder, "generated_video.mp4")

    frames = pipe(image, decode_chunk_size=decoding_t, generator=generator, motion_bucket_id=motion_bucket_id, noise_aug_strength=0.1, num_frames=25).frames[0]
    export_to_video(frames, video_path, fps=fps_id)
    torch.manual_seed(seed)

def convertVideoToGif():
    video_path = "outputs/generated_video.mp4"
    videoClip = VideoFileClip(video_path)
    gif_path = "outputs/generated_gif.gif"
    videoClip.write_gif(gif_path)
    return gif_path

def resize_image(image, output_size=(1024, 576)):
    # Calculate aspect ratios
    target_aspect = output_size[0] / output_size[1]  # Aspect ratio of the desired size
    image_aspect = image.width / image.height  # Aspect ratio of the original image

    # Resize then crop if the original image is larger
    if image_aspect > target_aspect:
        # Resize the image to match the target height, maintaining aspect ratio
        new_height = output_size[1]
        new_width = int(new_height * image_aspect)
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        # Calculate coordinates for cropping
        left = (new_width - output_size[0]) / 2
        top = 0
        right = (new_width + output_size[0]) / 2
        bottom = output_size[1]
    else:
        # Resize the image to match the target width, maintaining aspect ratio
        new_width = output_size[0]
        new_height = int(new_width / image_aspect)
        resized_image = image.resize((new_width, new_height), Image.LANCZOS)
        # Calculate coordinates for cropping
        left = 0
        top = (new_height - output_size[1]) / 2
        right = output_size[0]
        bottom = (new_height + output_size[1]) / 2

    # Crop the image
    cropped_image = resized_image.crop((left, top, right, bottom))
    return cropped_image

if __name__ == "__main__":
    prompt = ""
    num_inference_steps = 28
    guidance_scale = 7.5
    generateGif(prompt, num_inference_steps, guidance_scale)