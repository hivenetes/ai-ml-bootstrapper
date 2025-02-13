from crewai import Agent, Task
from openai import OpenAI
from crewai.tools import tool
import os
import streamlit as st

my_product = st.session_state.get("my_product")

@tool("Product Research Tool")
def ProductResearchTool(my_product: str) -> str:
    """
    Fetches the information about {my_product} from the GenAI Platform
    Args:
        my_product: The name of the product to research.

    Returns:
        str: The information about {my_product}.
    """

    agent_endpoint = os.getenv("GENAI_PRODUCT_RESEARCHER_AGENT_ENDPOINT")
    agent_key = os.getenv("GENAI_PRODUCT_RESEARCHER_AGENT_KEY")

    client = OpenAI(
        base_url = agent_endpoint,
        api_key = agent_key,
    )

    response = client.chat.completions.create(
        model = "DeepSeek R1 Distill Llama 70B",
        messages = [{"role": "user", "content": f"You are an expert Product Researcher.  You are expert at analyzing product features and capabilities using AI platforms. Your task is to Research and gather detailed information about {my_product} whose details will be available to you."}],
    )

    return response.choices[0].message.content
    

product_researcher = Agent(
    role="Product Researcher",
    goal="Conduct comprehensive research to gather in-depth information about {my_product}, focusing on its features and capabilities.",
    backstory="A seasoned expert in product analysis, leveraging advanced AI platforms to extract and synthesize detailed insights.",
    abilities=[ProductResearchTool],
    verbose=True
)

product_research_task = Task(
    description="Conduct a thorough investigation to compile detailed information on the features and capabilities of {my_product}.",
    expected_output="A comprehensive report detailing the features and capabilities of {my_product}.",
    agent=product_researcher,
    verbose=True
)