"""Configuration and environment setup."""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
_env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(_env_path)


def get_api_key() -> str:
    """Get x.ai API key from environment."""
    key = os.getenv("XAI_API_KEY")
    if not key:
        raise ValueError(
            "XAI_API_KEY not set. Create .env from .env.example and add your key from https://console.x.ai/"
        )
    return key


def get_model() -> str:
    """Get Grok model name."""
    return os.getenv("GROK_MODEL", "grok-4-1-fast-reasoning")
