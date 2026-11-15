
import os
import re
import json

from dotenv import load_dotenv
from google import genai
from google.genai import types

from app.tools import AVAILABLE_TOOLS

load_dotenv()

MODEL_NAME = "gemini-2.5-flash"

API_KEY = os.getenv("GEMINI_API_KEY")

client = None

if API_KEY:
    client = genai.Client(
        api_key=API_KEY,
        http_options=types.HttpOptions(api_version="v1beta")
    )

SYSTEM_INSTRUCTION = """
You are an AI assistant for an Internship Application and Tracking Portal.
Use the registered tools to retrieve student profiles, internship details,
and eligibility results. Never invent information.
Demo data is not officially verified. Never claim that a student can
officially proceed based on demo data.
"""

TOOL_DECLARATIONS = [
    types.FunctionDeclaration(
        name="read_student_profile",
        description="Retrieve a student profile using student ID.",
        parameters={
            "type": "OBJECT",
            "properties": {
                "student_id": {"type": "STRING"}
            },
            "required": ["student_id"]
        }
    ),
    types.FunctionDeclaration(
        name="read_opportunity",
        description="Retrieve an internship using opportunity ID.",
        parameters={
            "type": "OBJECT",
            "properties": {
                "opportunity_id": {"type": "STRING"}
            },
            "required": ["opportunity_id"]
        }
    ),
    types.FunctionDeclaration(
        name="check_eligibility",
        description="Check student eligibility for an internship.",
        parameters={
            "type": "OBJECT",
            "properties": {
                "student_id": {"type": "STRING"},
                "opportunity_id": {"type": "STRING"}
            },
            "required": ["student_id", "opportunity_id"]
        }
    )
]

AGENT_TOOLS = types.Tool(
    function_declarations=TOOL_DECLARATIONS
)

TOOL_CONFIG = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION,
    tools=[AGENT_TOOLS],
    temperature=0.2
)


def execute_tool(function_name: str, arguments: dict):
    """Execute only registered Python tools."""

    if function_name not in AVAILABLE_TOOLS:
        return {"error": f"Unknown tool: {function_name}"}

    try:
        result = AVAILABLE_TOOLS[function_name](**arguments)

        if hasattr(result, "model_dump"):
            return result.model_dump()

        return result

    except Exception as error:
        return {"error": str(error)}


def local_fallback(user_query: str) -> str:
    """
    Local execution when Gemini API quota is unavailable.
    Uses the same Python tools and JSON data.
    """

    query = user_query.lower()

    student_match = re.search(r"\bstu\d+\b", query, re.I)
    opportunity_match = re.search(r"\bint\d+\b", query, re.I)

    student_id = (
        student_match.group(0).upper()
        if student_match else "STU001"
    )

    opportunity_id = (
        opportunity_match.group(0).upper()
        if opportunity_match else "INT001"
    )

    if any(word in query for word in [
        "eligibility", "eligible", "qualify"
    ]) or query.strip() == "3":

        result = execute_tool(
            "check_eligibility",
            {
                "student_id": student_id,
                "opportunity_id": opportunity_id
            }
        )

        return (
            "LOCAL TOOL EXECUTION\n\n"
            "Eligibility Check\n"
            f"Student ID: {student_id}\n"
            f"Opportunity ID: {opportunity_id}\n\n"
            f"{json.dumps(result, indent=2)}\n\n"
            "Note: This is a demonstration result. "
            "Official verification is required before proceeding."
        )

    if any(word in query for word in [
        "profile", "student", "my details"
    ]) or query.strip() == "1":

        result = execute_tool(
            "read_student_profile",
            {"student_id": student_id}
        )

        return (
            "LOCAL TOOL EXECUTION\n\n"
            "Student Profile\n"
            f"{json.dumps(result, indent=2)}\n\n"
            "Note: Student information is demonstration data."
        )

    if any(word in query for word in [
        "internship", "opportunity", "opening"
    ]) or query.strip() == "2":

        result = execute_tool(
            "read_opportunity",
            {"opportunity_id": opportunity_id}
        )

        return (
            "LOCAL TOOL EXECUTION\n\n"
            "Internship Opportunity\n"
            f"{json.dumps(result, indent=2)}\n\n"
            "Note: Opportunity information is demonstration data."
        )

    return (
        "Gemini API quota is currently exhausted.\n"
        "You can still use local tools. Try:\n"
        "1. View student profile\n"
        "2. View internship opportunity\n"
        "3. Check eligibility"
    )


def run_agent(user_query: str) -> str:
    """Run Gemini function calling with local fallback."""

    if not user_query.strip():
        return "Please enter a question."

    if client is None:
        return local_fallback(user_query)

    try:
        chat = client.chats.create(
            model=MODEL_NAME,
            config=TOOL_CONFIG
        )

        response = chat.send_message(user_query)

        for _ in range(5):

            function_calls = response.function_calls

            if not function_calls:
                return response.text or "No response generated."

            tool_responses = []

            for function_call in function_calls:

                result = execute_tool(
                    function_call.name,
                    dict(function_call.args or {})
                )

                tool_responses.append(
                    types.Part.from_function_response(
                        name=function_call.name,
                        response={"result": result}
                    )
                )

            response = chat.send_message(tool_responses)

        return "Maximum tool-call limit reached."

    except Exception as error:

        error_message = str(error)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            print("\nGemini quota exhausted. Switching to local tools...")
            return local_fallback(user_query)

        return f"Agent error: {error_message}"
