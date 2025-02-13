from crewai import Agent, Task
from openai import OpenAI
from crewai_tools import ScrapeWebsiteTool
from pydantic import BaseModel, Field
from crewai.tools import tool
import streamlit as st
import os

@tool("Competitor Research Tool")
def CompetitorResearchTool() -> str:
    """
    
    Given the detailed information gathered from scraping the websites of competitor products, provide a detailed summary of the information to compare with the product we are building.
    
    Args:
        None

    Returns:
        str: The detailed information about competitor products to compare with the product we are building.
    """

    agent_endpoint = os.getenv("GENAI_COMPETITOR_RESEARCHER_AGENT_ENDPOINT")
    agent_key = os.getenv("GENAI_COMPETITOR_RESEARCHER_AGENT_KEY")

    client = OpenAI(
        base_url = agent_endpoint,
        api_key = agent_key,
    )

    competitor1 = st.session_state.get("competitor1")
    competitor2 = st.session_state.get("competitor2") 

    response = client.chat.completions.create(
        model = "DeepSeek R1 Distill Llama 70B",
        messages = [{"role": "user", "content": f"""You are an expert Competitor Analyst. Your goal is to gather detailed information about {competitor1} and {competitor2} products."""}],
    )

    return response.choices[0].message.content

competitor_analyst = Agent(
            role="Competitor Analyst",
            goal="Gather detailed information about {competitor1} and {competitor2} products. If the websites are blocked, use Wikipedia to gather information.  Check multiple websites if needed.",
            backstory="Expert at analyzing product features and capabilities using AI platforms",
            expected_output="Detailed information about {competitor1} and {competitor2} products",
            tools=[
                ScrapeWebsiteTool(name="Scrape Website Tool", description="Use this tool to scrape the website of competitor products."),
                CompetitorResearchTool
            ],
            verbose=True
        )

competitor_research_task = Task(
    description="Research and gather detailed information about {competitor1} and {competitor2} products",
    expected_output="Detailed information about {competitor1} and {competitor2} products",
    agent=competitor_analyst,
    verbose=True
)