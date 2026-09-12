import os

from agents import Agent
from dotenv import load_dotenv

from tools.web_scraper import scrape_webpage

load_dotenv()

MODEL = os.getenv("MODEL", "gpt-4o")


web_scraper_agent = Agent(
    name="Web Scraping Specialist",
    model=MODEL,
    instructions="""
You are the web scraping specialist.

Use your web scraping tool when the user provides a direct URL.
Extract and return the relevant page content for the coordinator to
analyze. Do not invent content that is not present on the page.
""",
    tools=[scrape_webpage],
)
