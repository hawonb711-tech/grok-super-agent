"""Computer Use 에이전트 루프 - 스냅샷 → AI 결정 → 액션 실행."""

import json
import re
from typing import Any

from src.computer_use.cup_client import CUPClient
from src.orchestrator.router import Router, ModelId
from src.llm_clients.grok_client import GrokClient
from src.llm_clients.claude_client import ClaudeClient
from src.llm_clients.openai_client import OpenAIClient


COMPUTER_USE_SYSTEM = """You are an AI that controls a computer via the Computer Use Protocol (CUP).

You receive:
1. A CUP snapshot of the current screen (compact tree of UI elements with IDs like e0, e1, e2...)
2. The user's current subtask

You must respond with a JSON object for the NEXT action. Format:
{"element_id": "e14", "action": "click"}
{"element_id": "e5", "action": "type", "value": "hello world"}
{"action": "press", "keys": "ctrl+s"}

Valid actions: click, type, toggle, press (for keyboard shortcuts without element).
If the task is complete, return: {"action": "done", "message": "summary"}
If you cannot determine the next step, return: {"action": "none", "message": "reason"}
"""


class ComputerUseLoop:
    """스냅샷 → 라우터 → AI → 액션 실행 루프."""

    def __init__(self) -> None:
        self.cup = CUPClient()
        self.router = Router()
        self._clients: dict[ModelId, Any] = {ModelId.GROK: GrokClient()}
        try:
            self._clients[ModelId.CLAUDE] = ClaudeClient()
        except ValueError:
            pass
        try:
            self._clients[ModelId.OPENAI] = OpenAIClient()
        except ValueError:
            pass

    def _get_client(self, model_id: ModelId):
        return self._clients.get(model_id) or self._clients[ModelId.GROK]

    def _parse_action(self, response: str) -> dict[str, Any] | None:
        """LLM 응답에서 액션 JSON 추출."""
        text = response.strip()
        # Try to find JSON object
        match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
        return None

    def _execute_action(self, action_spec: dict[str, Any]) -> tuple[bool, str]:
        """액션 실행."""
        act = action_spec.get("action", "")
        if act == "done":
            return True, action_spec.get("message", "Done")
        if act == "none":
            return False, action_spec.get("message", "No action")

        if act == "press":
            keys = action_spec.get("keys", "")
            if keys:
                result = self.cup.press(keys)
                return result["success"], result.get("message", "") or result.get("error", "")
            return False, "press requires 'keys'"

        element_id = action_spec.get("element_id", "")
        if not element_id:
            return False, "element_id required"
        value = action_spec.get("value", "")
        params = {"value": value} if value else {}
        result = self.cup.action(element_id, act, **params)
        return result["success"], result.get("message", "") or result.get("error", "")

    def run_step(self, task: str, max_iterations: int = 20) -> str:
        """단일 태스크에 대해 스냅샷→AI→액션 루프 실행."""
        for i in range(max_iterations):
            snapshot = self.cup.snapshot()
            model_id = self.router.route(task, snapshot)
            client = self._get_client(model_id)

            prompt = f"""CUP Snapshot (current screen):
{snapshot}

User subtask: {task}

What is the next CUP action? Respond with JSON only."""

            try:
                response = client.complete(prompt, system_prompt=COMPUTER_USE_SYSTEM)
            except Exception as e:
                return f"LLM error: {e}"

            action_spec = self._parse_action(response)
            if not action_spec:
                return f"Could not parse action from: {response[:200]}..."

            success, msg = self._execute_action(action_spec)
            if action_spec.get("action") == "done":
                return msg
            if not success:
                return f"Action failed: {msg}"
        return "Max iterations reached"

    def run(self, task: str, decompose: bool = False) -> str:
        """업무 실행. decompose=True면 하위 태스크로 분해 후 순차 실행."""
        if decompose:
            from src.orchestrator.task_decomposer import TaskDecomposer

            decomposer = TaskDecomposer()
            subtasks = decomposer.decompose(task)
            results = []
            for st in subtasks:
                r = self.run_step(st)
                results.append(r)
            return "\n".join(f"- {st}: {r}" for st, r in zip(subtasks, results))
        return self.run_step(task)
