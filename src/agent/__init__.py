# ./src/agent/__init__.py

"""
Agent module initializer.

This module exposes the core classes and common data types for building
an LLM-based agent with tool routing capabilities.

Exports:
    - AgentCLI: Command-line interface for interacting with the agent.
    - ToolAgent: Main agent class that manages conversation and tool calls.
    - LLMClient: Wrapper for sending messages to the Phi-3 API.
    - Messages, Message: Types representing chat messages and conversation
                         history.
    - Payload: Generic dictionary used for API requests or structured data.
"""

from .agent import ToolAgent
from .llm import LLMClient
from .cli import AgentCLI
from .common_data_types import Messages, Payload, Message

__all__ = [
    "AgentCLI",
    "ToolAgent",
    "LLMClient",
    "Messages",
    "Payload",
    "Message",
]
