# ./src/tools/tool_router.py

import re
import json
from typing import Dict, Any, Optional
from .tools import TOOLS

ToolData = Optional[Dict[str, Any]]
"""
Optional dictionary containing tool invocation data.

Expected keys:
    tool (str): Name of the tool to call.
    arguments (dict): Keyword arguments to pass to the tool function.

If no tool is invoked, this can be None.
"""


class ToolRouter:
    """
    Manages extraction of tool invocation instructions from LLM output
    and delegates execution to the corresponding tool.

    Responsibilities:
        - Parse JSON payloads from LLM responses containing tool calls.
        - Validate presence of required keys ("tool" and "arguments").
        - Execute the requested tool with provided arguments.

    Tools are registered in the global TOOLS dictionary.
    """

    @staticmethod
    def extract_json(text: str) -> ToolData:
        """
        Extract a tool invocation payload from a string.

        This method searches the text for a JSON object that contains
        the keys "tool" and "arguments". If such a JSON object is found
        and can be parsed, it is returned as a dictionary.

        Args:
            text: Raw string potentially containing a tool call JSON.

        Returns:
            A dictionary with tool invocation data if found, otherwise None.
        """
        result: ToolData = None
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                json_str = match.group(0).strip()
                parsed = json.loads(json_str)

                is_valid = isinstance(parsed, dict)
                has_tool = "tool" in parsed
                has_arguments = "arguments" in parsed

                if is_valid and has_tool and has_arguments:
                    result = parsed
            except json.JSONDecodeError:
                result = None

        return result

    @staticmethod
    def call_tool(tool_data: ToolData) -> str:
        """
        Execute a tool using the extracted tool invocation data.

        Args:
            tool_data: Dictionary containing:
                - "tool": str, name of the tool
                - "arguments": dict of keyword arguments for the tool

        Returns:
            str: Result of the tool execution as a string.

        Raises:
            ValueError: If `tool_data` is None or the tool name is
                        not registered in TOOLS.
        """
        result: str = "[Error: Tool not executed]"
        if tool_data is not None:
            tool_name = tool_data.get("tool")
            if tool_name is not None:
                method = TOOLS.get(tool_name)
                if method is None:
                    raise ValueError(f"Unknown tool: {tool_name}")
                arguments = tool_data.get("arguments", {})
                result = method(**arguments)

        return result
