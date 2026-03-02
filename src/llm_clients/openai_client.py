"""OpenAI (GPT) API 클라이언트."""

import os

from openai import OpenAI


def _get_api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY not set")
    return key


class OpenAIClient:
    """OpenAI API 클라이언트."""

    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI(api_key=_get_api_key())
        self.model = model

    def complete(self, prompt: str, system_prompt: str | None = None) -> str:
        """프롬프트에 대해 텍스트 완성."""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=4096,
        )
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content
        return ""
