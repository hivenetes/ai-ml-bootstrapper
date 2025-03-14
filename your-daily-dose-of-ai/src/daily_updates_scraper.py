from crewai import Agent, Task
from crewai_tools import ScrapeWebsiteTool
from crewai.tools import tool
from pydantic import BaseModel, Field
from typing import List
from src.ai_config import create_agent
import os
from openai import OpenAI

class DailyUpdates(BaseModel):
    title: str = Field(..., description="Title of the news")
    summary: str = Field(..., description="Summary of the news")
    url: str = Field(..., description="Url of the news")


class DailyUpdatesList(BaseModel):
    updates: List[DailyUpdates] = Field(..., description="List of daily updates")


@tool("Generate News Highlights")
def GenerateNewsHighlights() -> str:
    """
    From the content scraped, create news highlights.
    """

    agent_endpoint = os.getenv("GENAI_CURATE_HIGHLIGHTS_BASE_URL")
    agent_key = os.getenv("GENAI_CURATE_HIGHLIGHTS_API_KEY")

    client = OpenAI(
        base_url = agent_endpoint,
        api_key = agent_key,
    )

    response = client.chat.completions.create(
        model = "n/a",
        messages = [{"role": "user", "content": f"""You are an expert news highlights curator. Give me the highlights of the news from the content provided."""}],
    )

    return response.choices[0].message.content

daily_updates_scraper_agent = create_agent(
    role="Web Scraper",
    goal="Scrape the given URLs for latest news on AI and create detailed summaries",
    backstory="You are an expert Web Scraper who specializes in extracting and summarizing AI news content.",
    verbose=True
)

daily_updates_scrape_task = Task(
    description="""
    1. Scrape each URL provided in this comma separated list: {urls}.
    2. For each URL:
       - Extract the main article title
       - Create a comprehensive 3-4 sentence summary
       - Include the source URL
    3. Format the information into a structured list of updates.
    4. Ensure each update has a title, summary, and URL.
    """,
    expected_output="""
    You must return a list of updates where each update contains:
    - title: The main headline or title of the article
    - summary: A 3-4 sentence summary of the key points
    - url: The source URL
    
    Example format:
    {
        "updates": [
            {
                "title": "Major AI Breakthrough Announced",
                "summary": "Researchers have achieved a significant milestone in AI development. The new system demonstrates unprecedented capabilities in natural language understanding. This breakthrough could revolutionize how AI systems interact with humans.",
                "url": "https://example.com/ai-news"
            },
            // ... more updates ...
        ]
    }
    """,
    agent=daily_updates_scraper_agent,
    tools=[ScrapeWebsiteTool(urls="{urls}"), GenerateNewsHighlights],
    output_pydantic=DailyUpdatesList
)
