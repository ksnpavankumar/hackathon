import httpx

from langchain_core.tools import tool

from config.settings import (
    ATLASSIAN_DOMAIN,
    ATLASSIAN_EMAIL,
    ATLASSIAN_API_TOKEN,
)


def search_jira_tickets(search_query: str):

    url = (
        f"https://{ATLASSIAN_DOMAIN}"
        "/rest/api/3/search/jql"
    )

    safe_query = (
        search_query
        .replace("\\", "\\\\")
        .replace("'", "\\'")
    )

    jql = (
        f"summary ~ '{safe_query}' "
        f"OR description ~ '{safe_query}'"
    )

    params = {
        "jql": jql,
        "maxResults": 5,
        "fields": (
            "summary,status,assignee,"
            "priority,description"
        ),
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
                    f"Jira Search error "
                    f"{response.status_code}"
                ),
            }

        data = response.json()

        issues = []

        for item in data.get("issues", []):

            fields = item.get("fields", {})

            description = fields.get("description")

            if isinstance(description, dict):
                description = (
                    "Description available in Jira."
                )

            issues.append(
                {
                    "issue_key": item.get("key"),
                    "summary": fields.get("summary"),
                    "description": description,
                    "jira_status": (
                        fields.get("status", {})
                        .get("name")
                    ),
                    "assignee": (
                        fields.get("assignee", {})
                        .get("displayName", "Unassigned")
                    ),
                    "priority": (
                        fields.get("priority", {})
                        .get("name")
                    ),
                }
            )

        return {
            "status": "success",
            "matches": issues,
        }

    except Exception as exc:

        return {
            "status": "error",
            "message": str(exc),
        }


@tool
def search_jira(search_query: str) -> dict:
    """
    Search Jira for issues, incidents, projects,
    status, priority, assignee and work tracking
    information.

    Use this tool when the user asks about Jira
    or internal work items.
    """

    print(
        f"🔎 Jira search: {search_query}"
    )

    return search_jira_tickets(search_query)
