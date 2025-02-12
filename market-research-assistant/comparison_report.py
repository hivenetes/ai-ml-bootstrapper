from crewai import Agent, Task
from crewai.tools import tool
from pydantic import BaseModel, Field
from typing import List
import streamlit as st
import os
from openai import OpenAI
from competitor_research import competitor_research_task
from product_research import product_research_task

competitor1 = st.session_state.get("competitor1")
competitor2 = st.session_state.get("competitor2") 

class Comparison(BaseModel):
    Category: str = Field(..., description="Category of the comparison")
    My_Product: str = Field(..., description="Summary of My Product on the category")
    Competitor1: str = Field(..., description=f"Summary of {competitor1} on the category")
    Competitor2: str = Field(..., description=f"Summary of {competitor2} on the category")

class ComparisonList(BaseModel):
    comparisons: List[Comparison] = Field(..., description=f"List of comparisons between My Product and {competitor1} and {competitor2}")


@tool("Comparision Report Tool")
def ComparisionReportTool() -> str:
    """
    
    Given the detailed information about my product and competitor products, provide a detailed summary of the comparison between my product and competitors.
    
    Args:
        None

    Returns:
        str: The detailed comparison report between my product and competitors.
    """

    agent_endpoint = os.getenv("GENAI_COMPARISON_REPORT_AGENT_ENDPOINT")
    agent_key = os.getenv("GENAI_COMPARISON_REPORT_AGENT_KEY")

    client = OpenAI(
        base_url = agent_endpoint,
        api_key = agent_key,
    )

    response = client.chat.completions.create(
        model = "DeepSeek R1 Distill Llama 70B",
        messages = [{"role": "user", "content": f"""You are an expert Comparison Report Generator. Your goal is to generate a detailed comparison report between my product and competitors."""}],
    )

    return response.choices[0].message.content

comparison_analyst = Agent(
            role="Comparison Report Generator",
            goal=f"""Compare My Product and {competitor1} and {competitor2}.
""",
            backstory="Expert at analyzing product features and capabilities using AI platforms. You have information about my product and competitors",
            tools=[ComparisionReportTool],
            verbose=True
        )

comparison_research_task = Task(
    description="Compare and analyze My Product and competitors",
    agent=comparison_analyst,
    expected_output="""Detailed comparison report about My Product and competitors features and capabilities in a table format.
            You must return a list of comparisons in JSON format where each comparision contains:
            - Category : category the comparison is about
            - My_Product : Summary of My Product on the category
            - Competitor1 : Summary of Competitor 1 on the category
            - Competitor2 : Summary of Competitor 2 on the category

            Example Output:
            {
                "comparisons": [
                    {
                        "Category": "Integration Capabilities",
                        "My_Product": "Seamless integration with popular IDEs and workflows.",
                        "Competitor1": "Wide range of supported integrations but may require additional configuration.",
                        "Competitor2": "Limited integrations compared to peers."
                    },
                    {
                        "Category": "Support & Documentation",
                        "My_Product": "Extensive resources and community support available.",
                        "Competitor1": "Extensive resources and community support available.",
                        "Competitor2": "Basic support options and limited documentation."
                    }
                    # Add more comparisons as needed
                ]
            }
            """,
    output_pydantic=ComparisonList,
    context=[product_research_task, competitor_research_task],
    verbose=True
)