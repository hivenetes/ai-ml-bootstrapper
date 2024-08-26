import gradio as gr
from typing import Optional
import rag
import logging

logging.basicConfig(filename='app.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def get_answer(query: str) -> Optional[str]:
    """Get an answer for the given query."""
    logging.info(f"Received query: {query}")
    if query.strip():
        response = rag.get_response(query)
        logging.info(f"Response: {response}")
        return response
    else:
        logging.info("Empty query received, returning None")
        return None

def create_interface() -> gr.Blocks:
    """Create and return the Gradio interface."""
    with gr.Blocks() as demo:
        gr.Markdown("# Ask anything about GPU Droplets")
        
        with gr.Row():
            with gr.Column(scale=1):
                inp = gr.Textbox(label="Question", placeholder="What are GPU Droplets?")
                submit_btn = gr.Button("Submit")
            with gr.Column(scale=2):
                out = gr.Textbox(label="Answer")
        inp.submit(get_answer, inputs=inp, outputs=out)
        
        submit_btn.click(get_answer, inputs=inp, outputs=out)
        
    
    return demo

if __name__ == "__main__":
    interface = create_interface()
    interface.launch(server_name="0.0.0.0", server_port=7860)
    