import gradio as gr
from multi_prompt_gif_creator import get_animated_gif

with gr.Blocks() as demo:
    prompt = gr.Textbox(label="Enter your prompts seperated by ;")
    image = gr.Image(label="Generated Gif")
    generate_button = gr.Button("Generate Gif")

    generate_button.click(fn=get_animated_gif, inputs=prompt, outputs=image)

demo.launch()
