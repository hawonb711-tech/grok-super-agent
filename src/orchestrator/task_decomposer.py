"""태스크 분해기 - 복합 업무를 하위 단계로 분해."""

from src.llm_clients.grok_client import GrokClient


TASK_DECOMPOSER_SYSTEM = """You are a task decomposer. Given a user's high-level task, break it into ordered subtasks that can be executed one by one.

Return ONLY a JSON array of strings, one subtask per element. No explanation.
Example: ["Open Excel", "Read data from B2:B31", "Calculate sum", "Create PowerPoint slide", "Paste result"]
"""


class TaskDecomposer:
    """복합 업무 → 하위 단계 분해. 디폴트 Grok 사용."""

    def __init__(self) -> None:
        self._client = GrokClient()

    def decompose(self, task: str) -> list[str]:
        """태스크를 하위 단계 리스트로 분해."""
        prompt = f"User task: {task}\n\nReturn JSON array of subtasks:"
        try:
            import json

            response = self._client.complete(prompt, system_prompt=TASK_DECOMPOSER_SYSTEM)
            text = response.strip()
            start = text.find("[")
            end = text.rfind("]") + 1
            if start >= 0 and end > start:
                text = text[start:end]
            parsed = json.loads(text)
            if isinstance(parsed, list):
                return [str(s) for s in parsed]
        except Exception:
            pass
        return [task]  # fallback: single task
