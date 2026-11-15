
from datetime import datetime, timezone


class ExecutionEngine:

    def __init__(self, tool_manager, max_steps=5):
        self.tool_manager = tool_manager
        self.max_steps = max_steps
        self.execution_history = []

    def execute(self, tool_name, arguments=None):

        if len(self.execution_history) >= self.max_steps:
            return {
                "status": "limit_reached",
                "message": "Maximum execution steps reached."
            }

        record = {
            "tool": tool_name,
            "arguments": arguments or {},
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        try:
            result = self.tool_manager.execute_tool(
                tool_name,
                arguments
            )

            record["status"] = "success"
            record["result"] = result

            self.execution_history.append(record)

            return {
                "status": "success",
                "result": result
            }

        except Exception as error:
            record["status"] = "failed"
            record["error"] = str(error)

            self.execution_history.append(record)

            return {
                "status": "failed",
                "error": str(error)
            }

    def get_history(self):
        return self.execution_history
