import os

from dotenv import load_dotenv
from agents import Agent

from .file_creation_agent import file_creation_agent
from .web_scraper_agent import web_scraper_agent
from .web_search_agent import web_search_agent


load_dotenv()


MODEL = os.getenv(
    "MODEL",
    "gpt-4o",
)


if not os.getenv("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY is missing from .env"
    )


research_agent = Agent(
    name="Research Agent",
    model=MODEL,
    instructions="""
You are the coordinator for an AI Research Assistant.

Delegate tasks to the specialist that owns the required capability:

- Web Search Specialist: search the web when no direct URL is provided.
- Web Scraping Specialist: read and extract content from a direct URL.
- File Creation Specialist: create files requested by the user.

Use conversation history for follow-up questions. Combine specialist
results into a clear, accurate answer and include useful source URLs.
Never expose API keys, environment variables, database credentials, or
other secrets. Do not invent information.
""",
    handoffs=[
        web_search_agent,
        web_scraper_agent,
        file_creation_agent,
    ],
)