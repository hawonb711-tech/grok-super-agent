"""ReAct (Reasoning + Acting) agent loop with Grok API."""

from xai_sdk import Client
from xai_sdk.chat import system, tool_result, user
from xai_sdk.tools import code_execution, get_tool_call_type, web_search

from src.config import get_api_key, get_model
from src.tools.registry import execute_tool, get_tools


SYSTEM_PROMPT = """You are an autonomous Grok agent that can reason and act to complete tasks.

You have access to tools:
- web_search: Search the web for real-time information
- code_execution: Execute Python code (server-side, secure sandbox)
- file_read: Read file contents
- file_write: Write content to a file

Use the ReAct pattern: Think step by step, decide which tool to use, execute it, and continue until the task is complete.
If a tool fails, try an alternative approach or retry with different parameters.
"""


class ReActAgent:
    """Grok-native ReAct agent with tool calling."""

    def __init__(self, model: str | None = None):
        self.client = Client(api_key=get_api_key(), timeout=3600)
        self.model = model or get_model()
        tools_def, self.executors = get_tools()

        # Combine server-side tools (web_search, code_execution) with client-side (file_read, file_write)
        self.tools = [
            web_search(),
            code_execution(),
            *tools_def,
        ]

    def run(self, user_input: str, max_iterations: int = 10) -> str:
        """Run the agent until completion or max iterations."""
        chat = self.client.chat.create(
            model=self.model,
            messages=[system(SYSTEM_PROMPT)],
            tools=self.tools,
        )
        chat.append(user(user_input))

        for _ in range(max_iterations):
            response = chat.sample()
            chat.append(response)

            # Final response without tool calls
            if response.content and not response.tool_calls:
                return response.content

            if not response.tool_calls:
                return response.content or "No response."

            # Only client-side tools need manual execution; server-side are handled by x.ai
            for tc in response.tool_calls:
                if get_tool_call_type(tc) == "client_side_tool":
                    result = execute_tool(
                        tc.function.name,
                        tc.function.arguments or "{}",
                        self.executors,
                    )
                    chat.append(tool_result(result))

        return "Max iterations reached."
