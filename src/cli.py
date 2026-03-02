"""Grok Super Agent — Elon Musk style CLI."""

import sys
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.theme import Theme

# Elon / X.ai aesthetic: dark, minimal, cyan accent
THEME = Theme(
    {
        "info": "dim cyan",
        "success": "bold green",
        "warning": "bold yellow",
        "error": "bold red",
        "brand": "bold cyan",
        "x": "bold white on black",
    }
)

BANNER = r"""
[bold cyan]  GROK SUPER AGENT[/bold cyan]
[bold black on white] X [/bold black on white] [dim]x.ai . Tesla . SpaceX[/dim]

[dim]  Multi-AI orchestration . Computer Use . 1000% efficiency[/dim]
[dim]  Truth-seeking AI . Default: Grok[/dim]
"""


def _print_banner(console: Console) -> None:
    console.print(BANNER)
    console.print(
        Panel(
            "[dim]Multi-AI orchestration . Computer Use . Default Grok[/dim]",
            style="dim",
            border_style="cyan",
        )
    )


def run_react(console: Console) -> None:
    """ReAct 에이전트 모드."""
    from src.agent import ReActAgent

    agent = ReActAgent()
    console.print("\n[info]ReAct mode - web search, code exec, file read/write[/info]\n")

    while True:
        try:
            user_input = Prompt.ask("[bold cyan]You[/bold cyan]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "q"):
            console.print("[dim]Goodbye.[/dim]")
            break

        with console.status("[bold cyan]Thinking...[/bold cyan]", spinner="dots"):
            try:
                result = agent.run(user_input)
                console.print(Panel(Markdown(result), title="[bold cyan]Grok[/bold cyan]", border_style="cyan"))
            except Exception as e:
                console.print(f"[error]Error: {e}[/error]")


def run_computer_use(console: Console) -> None:
    """Computer Use 모드."""
    from src.orchestrator.loop import ComputerUseLoop

    loop = ComputerUseLoop()
    console.print("\n[info]Computer Use mode - screen control + multi-AI[/info]\n")

    while True:
        try:
            task = Prompt.ask("[bold cyan]Task[/bold cyan]").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[dim]Goodbye.[/dim]")
            break

        if not task:
            continue
        if task.lower() in ("exit", "quit", "q"):
            console.print("[dim]Goodbye.[/dim]")
            break

        with console.status("[bold cyan]Running...[/bold cyan]", spinner="dots"):
            try:
                result = loop.run(task, decompose=False)
                console.print(Panel(result, title="[bold cyan]Result[/bold cyan]", border_style="cyan"))
            except Exception as e:
                console.print(f"[error]Error: {e}[/error]")


def main() -> None:
    """Grok Super Agent 메인 진입점."""
    console = Console(theme=THEME, force_terminal=True)

    _print_banner(console)

    # Check .env
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        console.print(
            Panel(
                "[warning]XAI_API_KEY required[/warning]\n\n"
                "1. Copy .env.example to .env\n"
                "2. Get API key from https://console.x.ai/\n"
                "3. Add XAI_API_KEY=your_key to .env",
                title="[error]Setup required[/error]",
                border_style="red",
            )
        )
        sys.exit(1)

    # Mode selection
    console.print("\n[dim]Mode: [1] ReAct  [2] Computer Use  [q] Quit[/dim]")
    try:
        choice = Prompt.ask("[bold cyan]Select[/bold cyan]", default="1").strip().lower()
    except (EOFError, KeyboardInterrupt):
        sys.exit(0)

    if choice in ("q", "quit", "exit"):
        sys.exit(0)

    try:
        if choice == "2":
            run_computer_use(console)
        else:
            run_react(console)
    except ValueError as e:
        console.print(f"[error]{e}[/error]")
        sys.exit(1)
    except ImportError as e:
        console.print(f"[error]{e}[/error]")
        sys.exit(1)


if __name__ == "__main__":
    main()
