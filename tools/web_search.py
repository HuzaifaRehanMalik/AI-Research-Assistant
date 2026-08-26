import json
from ddgs import DDGS
from agents import function_tool


@function_tool
def web_search(query: str) -> str:
    """
    Search the web for information.

    Use this tool whenever the user asks about
    something on the internet but does NOT provide
    a direct URL.

    Returns the top search results including
    title, URL and snippet.
    """

    print(f"[WEB SEARCH] {query}")

    try:

        with DDGS() as ddgs:
            results = list(
                ddgs.text(
                    query,
                    max_results=5,
                )
            )

        if not results:
            return "No search results found."

        cleaned_results = []

        for result in results:

            cleaned_results.append(
                {
                    "title": result.get("title"),
                    "url": result.get("href"),
                    "snippet": result.get("body"),
                }
            )

        return json.dumps(
            cleaned_results,
            indent=2,
        )

    except Exception as e:

        return f"Web search failed:\n{str(e)}"