import torch
from PIL import Image
from diffusers import FluxPipeline
from diffusers import FluxImg2ImgPipeline
from diffusers import DiffusionPipeline
from pathlib import Path

def get_animated_gif(model_choice, prompts, num_inference_steps, guidance_scale, seed):
    images = []
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    if(model_choice == "Flux"):
        img_to_img_pipe = FluxImg2ImgPipeline.from_pretrained("black-forest-labs/FLUX.1-schnell", torch_dtype=torch.bfloat16)
        img_to_img_pipe = img_to_img_pipe.to(device)

        text_to_img_pipe = FluxPipeline.from_pretrained("black-forest-labs/FLUX.1-dev", torch_dtype=torch.bfloat16)
        text_to_img_pipe.enable_model_cpu_offload()

        previous_image = None
        for prompt in prompts:
            if previous_image is not None:
                image = img_to_img_pipe(
                    prompt=prompt, 
                    image=previous_image, 
                    num_inference_steps=num_inference_steps, 
                    strength=0.95, 
                    guidance_scale=guidance_scale, 
                    generator=torch.Generator(device).manual_seed(seed)
                    ).images[0]
            else:
                image = text_to_img_pipe(
                    prompt, 
                    num_inference_steps=num_inference_steps, 
                    guidance_scale=guidance_scale, 
                    generator=torch.Generator(device).manual_seed(seed)
                    ).images[0]
            images.append(image)
            previous_image = image  # Update the previous image
    else:
        pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16, use_safetensors=True, variant="fp16")
        pipe.to(device)

        previous_image = None
        for prompt in prompts:
            if previous_image is not None:
                image = pipe(
                    prompt=prompt, 
                    image=previous_image, 
                    num_inference_steps=num_inference_steps, 
                    strength=0.95, 
                    guidance_scale=guidance_scale, 
                    generator=torch.Generator(device).manual_seed(seed)
                    ).images[0]
            else:
                image = pipe(
                    prompt, 
                    num_inference_steps=num_inference_steps, 
                    guidance_scale=guidance_scale, 
                    generator=torch.Generator(device).manual_seed(seed)
                    ).images[0]
            images.append(image)
            previous_image = image  # Update the previous image        

    Path("images").mkdir(parents=True, exist_ok=True)

    for i, image in enumerate(images):
        image.save(f"images/image_{i}.png")

    image_files = [f"images/image_{i}.png" for i in range(len(prompts))]
    images = [Image.open(image_file) for image_file in image_files]

    images[0].save("images/multiple_prompt_output.gif", save_all=True, append_images=images[1:], duration=500, loop=0)

    return "images/multiple_prompt_output.gif"