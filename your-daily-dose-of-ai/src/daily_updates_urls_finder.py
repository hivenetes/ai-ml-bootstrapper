from crewai import Agent, Task, LLM
from pydantic import BaseModel, Field
from typing import List
from crewai_tools import SerperDevTool
import litellm
from litellm import CustomLLM, completion, get_llm_provider
from openai import OpenAI
import os

class DailyUpdatesUrls(BaseModel):
    urls: List[str] = Field(..., description="Urls which contains latest news on AI.")


daily_updates_finder = Agent(
    role="Daily Updates Finder",
    goal="Find the Urls which contains latest news on AI.",
    backstory="You are an expert Url finder who specializes in finding the Urls which contains latest news on AI.", 
    verbose=True
)

daily_updates_task = Task(
    description="Find the Urls which contains latest news on AI.",
    expected_output="List of URLs",
    agent=daily_updates_finder,
    tools=[SerperDevTool(query="latest AI news")],
    output_pydantic=DailyUpdatesUrls
)