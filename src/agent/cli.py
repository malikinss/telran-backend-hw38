# ./src/agent/cli.py

from .agent import ToolAgent
from utils import ThinkingDots


class AgentCLI:
    """
    Command-line interface (CLI) for interacting with a ToolAgent.

    Responsibilities:
        1. Handle user input and send it to the agent.
        2. Display a dynamic "thinking" indicator while waiting
           for agent replies.
        3. Print agent responses in a user-friendly format.
        4. Gracefully exit the session when user types 'exit'.

    Example:
        >>> cli = AgentCLI()
        >>> cli.run()
        Phi-3 simple chat. Type 'exit' to quit.
        You: What is the weather in Paris?
        Agent is thinking...
        Agent: {"result": "City: Paris ..."}
    """

    def __init__(self) -> None:
        """
        Initialize the CLI with a ToolAgent and ThinkingDots indicator.

        Attributes:
            agent (ToolAgent): The agent handling LLM communication
                               and tool execution.
            dots (ThinkingDots): Animated dots displayed while the agent
                                 is processing.
        """
        self.agent = ToolAgent()
        self.dots = ThinkingDots("Agent is thinking")

    def run(self) -> None:
        """
        Start the interactive command-line session.

        The loop continues until the user types 'exit'. For each user input:
            1. Starts the thinking dots animation.
            2. Sends the input to the agent and waits for a reply.
            3. Stops the animation once the reply is received.
            4. Displays the agent's response.

        Notes:
            - The session is terminated gracefully when 'exit' is entered.
            - All user inputs are stripped of leading/trailing whitespace.
        """
        print("Phi-3 simple chat. Type 'exit' to quit.")

        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "exit":
                print("Bye!")
                break

            self.dots.start()
            try:
                reply = self.agent.run(user_input)
            finally:
                self.dots.stop()

            print("\nAgent:", reply)
            print("_" * 60)
