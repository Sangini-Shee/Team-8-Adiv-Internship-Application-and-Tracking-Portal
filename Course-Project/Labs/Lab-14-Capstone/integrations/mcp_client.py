"""Small stdio MCP client for calling this project's MCP server."""
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_FILE = Path(__file__).resolve().parents[1] / "mcp_server.py"


async def _call_tool(tool_name: str, arguments: dict):
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_FILE)],
        env=None,
    )
    async with stdio_client(params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, arguments)
            return result


def call_mcp_tool(tool_name: str, arguments: dict | None = None):
    """Call a tool on the local MCP server and return text content."""
    result = asyncio.run(_call_tool(tool_name, arguments or {}))
    parts = []
    for item in getattr(result, "content", []):
        if getattr(item, "text", None):
            parts.append(item.text)
    return "\n".join(parts) if parts else str(result)
