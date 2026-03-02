"""Claude (Anthropic) API 클라이언트."""

import os

from anthropic import Anthropic


def _get_api_key() -> str:
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        raise ValueError("ANTHROPIC_API_KEY not set")
    return key


class ClaudeClient:
    """Claude API 클라이언트."""

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        self.client = Anthropic(api_key=_get_api_key())
        self.model = model

    def complete(self, prompt: str, system_prompt: str | None = None) -> str:
        """프롬프트에 대해 텍스트 완성."""
        kwargs = {"model": self.model, "max_tokens": 4096, "messages": [{"role": "user", "content": prompt}]}
        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)
        if response.content and len(response.content) > 0:
            return response.content[0].text
        return ""
