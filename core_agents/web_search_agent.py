import os

from agents import Agent
from dotenv import load_dotenv

from tools.web_search import web_search

load_dotenv()

MODEL = os.getenv("MODEL", "gpt-4o")


web_search_agent = Agent(
    name="Web Search Specialist",
    model=MODEL,
    instructions="""
You are the web search specialist.

Use your web search tool to find current information when the user
 does not provide a direct URL. Return concise results with useful
source URLs and do not invent information.
""",
    tools=[web_search],
)
