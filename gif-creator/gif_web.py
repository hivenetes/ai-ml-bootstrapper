import gradio as gr
import multi_prompt_gif_creator
import single_prompt_multiple_images_gif_creator

def get_gif_image(prompt):
    prompts_list = prompt.split(";")
    
    if len(prompts_list) == 1:
        return single_prompt_multiple_images_gif_creator.get_animated_gif(prompt)
    else:
        return multi_prompt_gif_creator.get_animated_gif(prompts_list)

with gr.Blocks() as demo:
    prompt = gr.Textbox(label="Enter single prompt or multiple prompts seperated by semicolon(;)")
    examples = gr.Examples(["A beautiful sunset", "Road in a forest"], prompt)

    image = gr.Image(label="Generated Gif", width=500, height=500)
    generate_button = gr.Button("Generate Gif")

    generate_button.click(fn=get_gif_image, inputs=prompt, outputs=image)

demo.launch()
