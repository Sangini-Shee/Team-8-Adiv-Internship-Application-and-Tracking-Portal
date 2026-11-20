# Framework integrations

## LangChain
- `langchain_agent.py` registers portal lookup and eligibility tools.
- Uses LangChain `create_agent()` and tool calling.
- Configure `GOOGLE_API_KEY` to enable LLM responses.
- The deterministic eligibility function remains authoritative.

## MCP
- `mcp_server.py` exposes `list_internships`, `get_student_profile`,
  and `verify_eligibility` as MCP tools using the official Python SDK v1 API.
- `mcp_client.py` demonstrates calling the local server over stdio.
- Start the standalone server with `python mcp_server.py`.

## Swarms
- `swarms_workflow.py` defines a real Swarms `SequentialWorkflow` with
  Academic, Skills and Career specialist agents.
- Configure a supported provider key and `SWARMS_MODEL` before running it.
- No model key is required for the core portal; local deterministic logic
  remains available.

LLM calls are optional and may incur provider charges or quota usage.
Human approval steps remain mandatory for application decisions.
