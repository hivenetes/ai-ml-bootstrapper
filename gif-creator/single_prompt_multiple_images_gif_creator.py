import torch
from PIL import Image
from diffusers import FluxPipeline
from diffusers import StableDiffusionPipeline
from pathlib import Path

def get_animated_gif(model_choice, prompt, num_inference_steps, guidance_scale, seed):
    # Set the seed for reproducibility
    torch.manual_seed(seed)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    if(model_choice == "Flux"):
        text_to_img_pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16)
        text_to_img_pipe.enable_model_cpu_offload()
    else:
        text_to_img_pipe = StableDiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16)
        text_to_img_pipe = text_to_img_pipe.to(device)
        
    # Generate images
    generated_images = text_to_img_pipe(
        prompt=prompt,
        num_images_per_prompt=4,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale
    ).images

    # Create a directory to save the images
    Path("images").mkdir(parents=True, exist_ok=True)

    # Save each generated image
    for i, image in enumerate(generated_images):
        image.save(f"images/image_{i}.png")

    # Open the saved images
    image_files = [f"images/image_{i}.png" for i in range(len(generated_images))]
    images = [Image.open(image_file) for image_file in image_files]

    # Save the images as a GIF
    gif_path = "images/animated_output.gif"
    images[0].save(gif_path, save_all=True, append_images=images[1:], duration=500, loop=0)

    return gif_path