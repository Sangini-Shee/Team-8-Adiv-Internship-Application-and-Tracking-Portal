
import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


SERVER_PATH = (
    Path(__file__).resolve().parents[1]
    / "server"
    / "mcp_server.py"
)


async def call_mcp_tool(tool_name, arguments=None):
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
        env=None
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            tools = await session.list_tools()
            tool_names = [tool.name for tool in tools.tools]

            assert tool_name in tool_names

            result = await session.call_tool(
                tool_name,
                arguments or {}
            )

            assert not result.isError

            return result


def test_mcp_server_discovers_tools():
    async def check():
        server_params = StdioServerParameters(
            command=sys.executable,
            args=[str(SERVER_PATH)],
            env=None
        )

        async with stdio_client(server_params) as (read_stream, write_stream):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()

                response = await session.list_tools()
                names = [tool.name for tool in response.tools]

                assert "get_student_profile" in names
                assert "list_internships" in names
                assert "get_internship_details" in names

    asyncio.run(check())


def test_get_student_profile():
    result = asyncio.run(
        call_mcp_tool(
            "get_student_profile",
            {"student_id": "STU001"}
        )
    )

    assert result.content
    assert "STU001" in result.content[0].text


def test_list_internships():
    result = asyncio.run(
        call_mcp_tool("list_internships")
    )

    assert result.content
    assert "INT001" in result.content[0].text


def test_get_internship_details():
    result = asyncio.run(
        call_mcp_tool(
            "get_internship_details",
            {"internship_id": "INT001"}
        )
    )

    assert result.content
    assert "INT001" in result.content[0].text
