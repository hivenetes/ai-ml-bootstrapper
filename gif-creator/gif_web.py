import gradio as gr
from multi_prompt_gif_creator import get_animated_gif

with gr.Blocks() as demo:
    prompt = gr.Textbox(label="Enter your prompts seperated by semicolon (;)")
    examples = gr.Examples([["A beautiful sunset over the mountains; A sunset over the ocean; A sunset with colorful clouds; A sunset with a red sky"]], prompt)

    image = gr.Image(label="Generated Gif", width=500, height=500)
    generate_button = gr.Button("Generate Gif")

    generate_button.click(fn=get_animated_gif, inputs=prompt, outputs=image)

demo.launch()
