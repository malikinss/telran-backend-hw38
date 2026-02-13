# ./src/agent/llm.py

import os
import requests
from .common_data_types import Messages, Payload

URL = "PHI3_API_URL"
MODEL_NAME = "PHI3_MODEL_NAME"


class LLMClient:
    """
    A client for interacting with the Phi-3 large language model API.

    This class encapsulates sending conversation history to the Phi-3 API
    and retrieving textual responses. It handles HTTP requests, response
    parsing, and error propagation.

    Attributes:
        url (str): The base URL of the Phi-3 API endpoint.
        model (str): The name of the model to use for responses.

    Example:
        >>> client = LLMClient()
        >>> messages = [{"role": "system", "content": "You are helpful."},
                        {"role": "user", "content": "Hello"}]
        >>> reply = client.send(messages)
        >>> print(reply)
    """

    def __init__(self) -> None:
        """
        Initialize the LLM client.

        Args:
            url (str): API endpoint URL. Defaults to the configured URL
                       in config.py.
            model (str): Model name to use. Defaults to MODEL_NAME
                         in config.py.
        """
        self.url: str = os.getenv(URL)  # type: ignore
        self.model: str = os.getenv(MODEL_NAME)     # type: ignore

    def send(self, messages: Messages) -> str:
        """
        Send conversation messages to the Phi-3 API and retrieve a response.

        The messages must be a list of dictionaries with 'role' and 'content'
        keys.

        Args:
            messages (Messages): Ordered list of messages representing the
                                 conversation history. Each message is a dict
                                 with keys 'role' ('user'|'assistant'|'system')
                                 and 'content' (str).

        Returns:
            str: The assistant's reply content returned by the API.

        Raises:
            requests.HTTPError: If the HTTP request fails (non-2xx response).
            KeyError: If the response does not contain 'message.content'.
        """
        payload: Payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }

        resp = requests.post(self.url, json=payload)
        resp.raise_for_status()

        data = resp.json()
        try:
            return data["message"]["content"]
        except KeyError:
            raise KeyError(
                "Invalid response structure: 'message.content' key is missing."
            )
