import gradio as gr
import image_to_gif_creator

def get_gif_image(prompt, num_inference_steps, guidance_scale, seed):
    if not prompt:
        raise gr.Error("Invalid input: The prompt should not be empty")
    else:
        return image_to_gif_creator.generateGif(prompt, num_inference_steps, guidance_scale, seed)

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
        # Animated GIF Generator
        """
    )

    with gr.Row():
        with gr.Column(scale=2):
            prompt = gr.Textbox(
                label="Enter prompt",
                placeholder="e.g., An animated panda dancing"
            )
            examples = gr.Examples(
                examples=[
                    "An animated castle with clouds",
                    "An animated panda dancing",
                    "An animated tortoise crossing the road"
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
                value=7.5,
                step=0.5
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
        inputs=[prompt, num_inference_steps, guidance_scale, seed],
        outputs=image
    )

demo.launch(server_name="0.0.0.0", server_port=7860)