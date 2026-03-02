"""Tool registry - builds xai_sdk tool definitions and executor map."""

import json
from typing import Any

from xai_sdk.chat import tool

from src.tools.file_ops import FileReadTool, FileWriteTool


def get_tools() -> tuple[list, dict[str, callable]]:
    """
    Return (xai_sdk tool definitions, executor map).
    Executor map: tool_name -> callable that executes and returns str.
    """
    file_read = FileReadTool()
    file_write = FileWriteTool()

    tools_def = [
        tool(
            name=file_read.name,
            description=file_read.description,
            parameters=file_read.parameters,
        ),
        tool(
            name=file_write.name,
            description=file_write.description,
            parameters=file_write.parameters,
        ),
    ]

    executors = {
        file_read.name: file_read.execute,
        file_write.name: file_write.execute,
    }

    return tools_def, executors


def execute_tool(name: str, arguments: str, executors: dict[str, callable]) -> str:
    """Execute a tool by name with JSON arguments."""
    if name not in executors:
        return f"Error: Unknown tool '{name}'"
    try:
        args = json.loads(arguments) if arguments else {}
        return executors[name](**args)
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON arguments: {e}"
    except Exception as e:
        return f"Error executing {name}: {e}"
