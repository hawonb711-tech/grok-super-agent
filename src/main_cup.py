"""Computer Use + 멀티 AI 오케스트레이션 CLI."""

import sys

from src.orchestrator.loop import ComputerUseLoop


def main() -> None:
    """Computer Use 에이전트 실행."""
    print("Computer Use + 멀티 AI 오케스트레이터")
    print("업무를 입력하세요. 'exit'로 종료.\n")

    try:
        loop = ComputerUseLoop()
    except ImportError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    while True:
        try:
            task = input("업무: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n종료.")
            break

        if not task:
            continue
        if task.lower() in ("exit", "quit", "q"):
            print("종료.")
            break

        print("\n실행 중...")
        try:
            result = loop.run(task, decompose=False)
            print(f"\n결과: {result}\n")
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
