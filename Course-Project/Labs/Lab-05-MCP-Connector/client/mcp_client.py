
import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

SERVER_PATH = Path(__file__).resolve().parents[1] / "server" / "mcp_server.py"


async def run_mcp_client():
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_PATH)],
        env=None
    )

    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:

            await session.initialize()

            print("\n===== INTERNSHIP PORTAL MCP CLIENT =====")

            tools_response = await session.list_tools()

            print("\nAvailable MCP Tools:")
            for tool in tools_response.tools:
                print(f"- {tool.name}: {tool.description}")

            print("\n1. Get Student Profile")
            print("2. List Internships")
            print("3. Get Internship Details")

            choice = input("\nChoose an option: ").strip()

            if choice == "1":
                student_id = input("Enter Student ID: ").strip()
                tool_name = "get_student_profile"
                arguments = {"student_id": student_id}

            elif choice == "2":
                tool_name = "list_internships"
                arguments = {}

            elif choice == "3":
                internship_id = input("Enter Internship ID: ").strip()
                tool_name = "get_internship_details"
                arguments = {"internship_id": internship_id}

            else:
                print("Invalid option.")
                return

            result = await session.call_tool(tool_name, arguments)

            print("\nMCP Tool Result:")
            for item in result.content:
                if hasattr(item, "text"):
                    try:
                        parsed = json.loads(item.text)
                        print(json.dumps(parsed, indent=4))
                    except json.JSONDecodeError:
                        print(item.text)

            if result.isError:
                print("\nThe MCP tool returned an error.")


if __name__ == "__main__":
    asyncio.run(run_mcp_client())
