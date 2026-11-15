
from runtime.tool_manager import ToolManager
from runtime.execution_engine import ExecutionEngine


class AgentRuntime:

    def __init__(self, max_steps=5):
        self.tool_manager = ToolManager()
        self.engine = ExecutionEngine(
            self.tool_manager,
            max_steps=max_steps
        )

    def register_tool(self, name, function, description=""):
        self.tool_manager.register_tool(
            name,
            function,
            description
        )

    def run(self, task, tool_name, arguments=None):

        if not task or not task.strip():
            return {
                "status": "failed",
                "error": "Task description cannot be empty."
            }

        result = self.engine.execute(
            tool_name,
            arguments
        )

        return {
            "task": task,
            "status": result["status"],
            "result": result.get("result"),
            "error": result.get("error")
        }

    def get_available_tools(self):
        return self.tool_manager.list_tools()

    def get_execution_history(self):
        return self.engine.get_history()
