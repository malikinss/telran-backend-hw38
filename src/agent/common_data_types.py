# ./src/agent/common_data_types.py

from typing import List, Dict, Any

Message = Dict[str, str]
"""
Represents a single chat message.

Keys:
    role (str): Role of the message sender
                ('user', 'assistant', 'system', 'tool').
    content (str): Text content of the message.
"""

Messages = List[Message]
"""
List of chat messages representing conversation history.

Used to maintain context across LLM calls.
"""

Payload = Dict[str, Any]
"""
Generic dictionary representing API request payload or arbitrary
key-value data.

Often used when sending structured data to tools or APIs.
"""
