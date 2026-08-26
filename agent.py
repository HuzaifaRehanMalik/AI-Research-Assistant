import os

from dotenv import load_dotenv
from agents import Agent

from tools.web_search import web_search
from tools.web_scraper import scrape_webpage
from tools.file_making import file_tool
# Load environment variables
load_dotenv()

# Read values from .env
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL", "gpt-4o")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env")

# Create the research agent
research_agent = Agent(
    name="Research Agent",

    model=MODEL,

    instructions="""
You are an AI Research Assistant.

You have access to two tools:

1. web_search
   - Use this when the user asks for information from the web but does not provide a URL.

2. scrape_webpage
   - Use this whenever the user provides a URL.
   - Read the webpage before answering.
3. file_tool
   - You can use this tool to create files with any type of data.
   - Use this tool to save the content you have generated or scraped into a file and save it in createdFile.
Rules:
- If the prompt contains a URL, use scrape_webpage.
- Otherwise, use web_search.
- Use previous conversation history when answering follow-up questions.
- Never invent facts.
- Always provide accurate answers.
- Include source URLs whenever possible.
""",

    tools=[
        web_search,
        scrape_webpage,
        file_tool,
        
    ],
)