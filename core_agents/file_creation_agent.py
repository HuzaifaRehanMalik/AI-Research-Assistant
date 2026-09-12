import os

from agents import Agent
from dotenv import load_dotenv

from tools.file_making import file_tool

load_dotenv()

MODEL = os.getenv("MODEL", "gpt-4o")


file_creation_agent = Agent(
    name="File Creation Specialist",
    model=MODEL,
    instructions="""
You are the file creation specialist.

Use your file creation tool when the user asks to create or save a
file. Keep all files inside createdFile/ and report the resulting path.
""",
    tools=[file_tool],
)
