import httpx

from langchain_core.tools import tool

from config.settings import (
    ATLASSIAN_DOMAIN,
    ATLASSIAN_EMAIL,
    ATLASSIAN_API_TOKEN,
)


def search_confluence_pages(search_query: str):

    url = (
        f"https://{ATLASSIAN_DOMAIN}"
        "/wiki/rest/api/content/search"
    )

    params = {
        "cql": f'text ~ "{search_query}"',
        "limit": 5,
    }

    auth = (
        ATLASSIAN_EMAIL.strip(),
        ATLASSIAN_API_TOKEN.strip(),
    )

    try:

        with httpx.Client() as client:

            response = client.get(
                url,
                params=params,
                auth=auth,
                timeout=10,
            )

        if response.status_code != 200:

            return {
                "status": "error",
                "message": (
                    f"Confluence Search error "
                    f"{response.status_code}"
                ),
            }

        data = response.json()

        pages = []

        for item in data.get("results", []):

            pages.append(
                {
                    "title": item.get("title"),
                    "type": item.get("type"),
                    "url": (
                        f"https://{ATLASSIAN_DOMAIN}"
                        "/wiki"
                        f"{item.get('_links', {}).get('webui', '')}"
                    ),
                }
            )

        return {
            "status": "success",
            "pages": pages,
        }

    except Exception as exc:

        return {
            "status": "error",
            "message": str(exc),
        }


@tool
def search_confluence(search_query: str) -> dict:
    """
    Search Confluence for internal documentation,
    architecture guides, runbooks, policies and
    technical documentation.
    """

    print(
        f"📚 Confluence search: {search_query}"
    )

    return search_confluence_pages(
        search_query
    )
