import torch
from PIL import Image
from diffusers import DiffusionPipeline
from pathlib import Path

pipe = DiffusionPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell")
pipe = pipe.to("cuda")

def get_animated_gif(prompts):
    images = []

    for prompt in prompts:
        image = pipe(prompt).images[0]
        images.append(image)

    Path("images").mkdir(parents=True, exist_ok=True)

    for i, image in enumerate(images):
        image.save(f"images/image_{i}.png")

    image_files = [f"images/image_{i}.png" for i in range(len(prompts))]
    images = [Image.open(image_file) for image_file in image_files]

    images[0].save("images/animated_output.gif", save_all=True, append_images=images[1:], duration=500, loop=0)

    return Image("images/animated_output.gif")