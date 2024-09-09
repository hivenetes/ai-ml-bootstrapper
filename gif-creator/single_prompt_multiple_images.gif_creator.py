import torch
from PIL import Image
from diffusers import FluxPipeline
from pathlib import Path
from diffusers.utils import export_to_gif

def get_animated_gif(prompt):
    images = []
    
    text_to_img_pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16)
    text_to_img_pipe.enable_model_cpu_offload()

    generated_images = text_to_img_pipe(prompt=prompt, num_images_per_prompt=4).images

    Path("images").mkdir(parents=True, exist_ok=True)

    for i, image in enumerate(generated_images):
        image.save(f"images/image_{i}.png")

    image_files = [f"images/image_{i}.png" for i in range(4)]
    images = [Image.open(image_file) for image_file in image_files]

    export_to_gif(images, "images/single_prompt_output.gif", fps=4)

    return "images/single_prompt_output.gif"