import gradio as gr
import multi_prompt_gif_creator
import single_prompt_multiple_images_gif_creator
import single_prompt_single_image_gif_creator

def get_gif_image(model_choice, prompt, num_inference_steps, guidance_scale, seed, num_images):
    prompts_list = prompt.split(";")
    
    prompts_list = [p.strip() for p in prompts_list if p.strip()]
    if not prompts_list:
        raise gr.Error("Invalid input: The prompt should not be empty or contain only separators.")
    else:
        if len(prompts_list) == 1:
            if num_images == 1:
                return single_prompt_single_image_gif_creator.predict(model_choice, prompt, num_inference_steps, guidance_scale, seed)
            else:
                return single_prompt_multiple_images_gif_creator.get_animated_gif(model_choice, prompt, num_inference_steps, guidance_scale, seed, num_images)
        else:
            return multi_prompt_gif_creator.get_animated_gif(model_choice, prompts_list, num_inference_steps, guidance_scale, seed)

css="""
#col-container {
    margin: 0 auto;
    max-width: 520px;
}
#stills{max-height:160px}
"""

with gr.Blocks(css=css) as demo:
    gr.Markdown(
        """
        # GIF Generator
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            model_choice = gr.Dropdown(
                label="Choose Model",
                choices=["Flux", "Stable Diffusion"],
                value="Flux"
            )
            prompt = gr.Textbox(
                label="Enter single prompt or multiple prompts separated by semicolon (;)",
                placeholder="e.g., A beautiful sunset; A sunset over the ocean",
                lines=3
            )
            examples = gr.Examples(
                examples=[
                    "A beautiful sunset",
                    "A beautiful sunset over the mountains; A sunset over the ocean; A sunset with colorful clouds; A sunset with a red sky"
                ],
                inputs=prompt,
                label="Examples"
            )            
            num_inference_steps = gr.Slider(
                label="Number of Inference Steps",
                minimum=1,
                maximum=50,
                value=28,
                step=1
            )
            guidance_scale = gr.Slider(
                label="Guidance Scale",
                minimum=0.0,
                maximum=10.0,
                value=3.5,
                step=0.5
            )
            seed = gr.Number(
                label="Seed",
                value=0,
                precision=0
            )
            num_images = gr.Slider(
                label="Number of Images",
                minimum=1,
                maximum=10,
                value=4,
                step=1
            )
            generate_button = gr.Button("Generate GIF", variant="primary")

        with gr.Column(scale=1, min_width=500):
            image = gr.Image(label="Generated GIF", width=500, height=500)

    generate_button.click(
        fn=get_gif_image,
        inputs=[model_choice, prompt, num_inference_steps, guidance_scale, seed, num_images],
        outputs=image
    )

demo.launch()