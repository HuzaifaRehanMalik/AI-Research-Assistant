from pathlib import Path

from agents import function_tool

BASE_DIR = Path(__file__).resolve().parent.parent

CREATED_FILES_DIR = BASE_DIR / "createdFile"

CREATED_FILES_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


@function_tool
def file_tool(
    content: str,
    fileName: str,
):
    """
    Create a file inside createdFile.

    Files cannot be created outside the
    createdFile directory.
    """

    if not fileName:
        return "Error: fileName cannot be empty."

    safe_name = Path(fileName).name

    if safe_name in {
        "",
        ".",
        "..",
    }:
        return "Error: invalid file name."

    file_path = CREATED_FILES_DIR / safe_name

    try:
        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as file:
            file.write(content)

        return f"File created successfully: createdFile/{safe_name}"

    except Exception as error:  # noqa: BLE001 - tool returns creation errors to the agent.
        return f"Failed to create file: {error}"
