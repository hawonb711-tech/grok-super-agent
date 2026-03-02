"""Grok (x.ai) API 클라이언트."""

import os

from xai_sdk import Client
from xai_sdk.chat import system, user


def _get_api_key() -> str:
    key = os.getenv("XAI_API_KEY")
    if not key:
        raise ValueError("XAI_API_KEY not set")
    return key


class GrokClient:
    """Grok API 클라이언트."""

    def __init__(self, model: str | None = None):
        self.client = Client(api_key=_get_api_key(), timeout=3600)
        self.model = model or os.getenv("GROK_MODEL", "grok-4-1-fast-reasoning")

    def complete(self, prompt: str, system_prompt: str | None = None) -> str:
        """프롬프트에 대해 텍스트 완성."""
        messages = []
        if system_prompt:
            messages.append(system(system_prompt))
        messages.append(user(prompt))

        chat = self.client.chat.create(model=self.model, messages=messages)
        response = chat.sample()
        return response.content or ""
