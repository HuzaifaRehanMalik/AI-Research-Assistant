from agents import function_tool
from pathlib import Path


@function_tool
def file_tool(content: str, fileName: str):
    """Create a file only inside the createdFile folder."""

    base_folder = Path("createdFile")
    base_folder.mkdir(exist_ok=True)

    file_path = base_folder / Path(fileName).name

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return f"File created successfully: {file_path}"