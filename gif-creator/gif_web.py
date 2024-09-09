import gradio as gr
import multi_prompt_gif_creator
import single_prompt_multiple_images_gif_creator

def get_gif_image(prompt):
    prompts_list = prompt.split(";")
    
    prompts_list = [p.strip() for p in prompts_list if p.strip()]
    if not prompts_list:
        raise gr.Error("Invalid input: The prompt should not be empty or contain only separators.")
    else:
        if len(prompts_list) == 1:
            return single_prompt_multiple_images_gif_creator.get_animated_gif(prompt)
        else:
            return multi_prompt_gif_creator.get_animated_gif(prompts_list)

with gr.Blocks() as demo:
    gr.Markdown(
        """
        # GIF Generator
        Enter a single prompt or multiple prompts separated by semicolons (`;`) to generate a GIF.
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
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
            generate_button = gr.Button("Generate GIF", variant="primary")

        with gr.Column(scale=1):
            image = gr.Image(label="Generated GIF")

    generate_button.click(fn=get_gif_image, inputs=prompt, outputs=image)

demo.launch()