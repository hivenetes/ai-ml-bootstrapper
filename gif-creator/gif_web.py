import gradio as gr
import multi_prompt_gif_creator
import single_prompt_multiple_images_gif_creator

def get_gif_image(model_choice, prompt, num_inference_steps, guidance_scale, seed):
    prompts_list = prompt.split(";")
    
    prompts_list = [p.strip() for p in prompts_list if p.strip()]
    if not prompts_list:
        raise gr.Error("Invalid input: The prompt should not be empty or contain only separators.")
    else:
        if len(prompts_list) == 1:
            return single_prompt_multiple_images_gif_creator.get_animated_gif(model_choice, prompt, num_inference_steps, guidance_scale, seed)
        else:
            return multi_prompt_gif_creator.get_animated_gif(model_choice, prompts_list, num_inference_steps, guidance_scale, seed)

with gr.Blocks() as demo:
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
                value=25,
                step=1
            )
            guidance_scale = gr.Slider(
                label="Guidance Scale",
                minimum=0.0,
                maximum=10.0,
                value=7.5,
                step=1.0
            )
            seed = gr.Number(
                label="Seed",
                value=42,
                precision=0
            )
            generate_button = gr.Button("Generate GIF", variant="primary")

        with gr.Column(scale=1, min_width=500):
            image = gr.Image(label="Generated GIF", width=500, height=500)

    generate_button.click(
        fn=get_gif_image,
        inputs=[model_choice, prompt, num_inference_steps, guidance_scale, seed],
        outputs=image
    )

demo.launch()