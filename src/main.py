"""CLI entry point for the agentic autonomous system."""

import sys

from src.agent import ReActAgent


def main() -> None:
    """Run interactive CLI."""
    print("Agentic Autonomous System — Grok-Native ReAct Agent")
    print("Type your task and press Enter. Type 'exit' to quit.\n")

    try:
        agent = ReActAgent()
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "q"):
            print("Goodbye.")
            break

        print("\nThinking...")
        try:
            result = agent.run(user_input)
            print(f"\nAgent: {result}\n")
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
