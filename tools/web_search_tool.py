import os

from dotenv import load_dotenv
from ddgs import DDGS
from langchain_core.tools import tool

load_dotenv()


@tool
def search_web(query: str) -> str:
    """
    Search the live web for recent security
    vulnerabilities, CVEs, patches, vendor advisories
    and technical security information.
    """

    try:

        print(
            f"🌐 Web search: {query}"
        )

        with DDGS() as ddgs:

            results = list(
                ddgs.text(
                    query,
                    max_results=5
                )
            )

        if not results:
            return "No web results found."

        formatted = []

        for item in results:

            formatted.append(
                f"""
Title: {item.get("title")}
Snippet: {item.get("body")}
URL: {item.get("href")}
"""
            )

        return "\n---\n".join(
            formatted
        )

    except Exception as exc:

        print(
            f"Web search error: {exc}"
        )

        return (
            f"Error executing web search: "
            f"{exc}"
        )
