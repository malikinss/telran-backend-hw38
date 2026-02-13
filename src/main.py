# ./src/main.py

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file


def main() -> None:
    from agent import AgentCLI
    cli = AgentCLI()
    cli.run()


if __name__ == "__main__":
    main()
