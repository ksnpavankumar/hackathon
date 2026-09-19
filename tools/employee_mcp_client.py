import asyncio

from fastmcp import Client


EMPLOYEE_MCP_URL = "http://localhost:8000/mcp"


async def call_employee_mcp(
    tool_name: str,
    arguments: dict
):

    async with Client(EMPLOYEE_MCP_URL) as client:

        result = await client.call_tool(
            tool_name,
            arguments
        )

        return result.data


def run_employee_mcp(
    tool_name: str,
    arguments: dict
):

    return asyncio.run(
        call_employee_mcp(
            tool_name,
            arguments
        )
    )
