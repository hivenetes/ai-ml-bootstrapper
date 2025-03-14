from crewai import Agent, Task
from crewai.tools import tool
from gtts import gTTS
from datetime import datetime
import os
import streamlit as st
from pydantic import BaseModel, Field
from src.ai_config import create_agent

class AudioFile(BaseModel):
    audio_filename: str = Field(..., description="Name of the audio file")

@tool("Podcast Tool")
def podcast_tool(contents: str) -> AudioFile:
    """
    Converts the contents into a podcast audio file.

    Args:
        contents (str): The contents to be converted.

    Returns:
        AudioFile: The path to the generated podcast audio file.
    """

    username = st.session_state["username"]
    
    if st.session_state["use_saved_urls"]:
        audio_filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{username}_custom.mp3"
    else:
        audio_filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{username}_daily.mp3"
    
    audio_file_path = os.path.join("audio_files", audio_filename)

    tts = gTTS(text=contents, lang="en")
    tts.save(audio_file_path)
    return AudioFile(audio_filename=audio_filename)

podcast_agent = create_agent(
    role="Daily Updates Podcast Creator",
    goal="Create a podcast based on the daily updates",
    backstory="You are an expert Podcast Creator who specializes in creating a podcast based on the daily updates",
    verbose=True,
)

podcast_task = Task(
    description="Create a podcast based on the below contents: {contents}.",
    expected_output="An mp3 audio file of the podcast.",
    agent=podcast_agent,
    output_pydantic=AudioFile,
    tools=[podcast_tool],
)