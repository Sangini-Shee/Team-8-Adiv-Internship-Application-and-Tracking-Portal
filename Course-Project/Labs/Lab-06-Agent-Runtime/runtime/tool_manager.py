
class ToolManager:

    def __init__(self):
        self.tools = {}

    def register_tool(self, name, function, description=""):
        if not name or not callable(function):
            raise ValueError("A valid tool name and function are required.")

        self.tools[name] = {
            "function": function,
            "description": description
        }

    def list_tools(self):
        return [
            {
                "name": name,
                "description": details["description"]
            }
            for name, details in self.tools.items()
        ]

    def execute_tool(self, name, arguments=None):
        if name not in self.tools:
            raise ValueError(f"Tool '{name}' is not registered.")

        arguments = arguments or {}

        return self.tools[name]["function"](**arguments)
