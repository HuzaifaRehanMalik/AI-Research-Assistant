import httpx
import trafilatura
from agents import function_tool


@function_tool
def scrape_webpage(url: str) -> str:
    """
    Scrape and extract the readable content from a webpage.

    Use this tool whenever the user provides
    a direct URL.

    Returns clean article/page text.
    """

    print(f"[SCRAPER] {url}")

    try:

        response = httpx.get(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
            timeout=30,
            follow_redirects=True,
        )

        response.raise_for_status()

        downloaded = response.text

        extracted = trafilatura.extract(
            downloaded,
            include_links=True,
            include_images=False,
            include_tables=True,
            favor_precision=True,
        )

        if not extracted:

            return "No readable content could be extracted."

        return extracted

    except Exception as e:

        return f"Web scraping failed:\n{str(e)}"