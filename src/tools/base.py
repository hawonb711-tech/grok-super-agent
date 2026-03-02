"""Base tool interface."""

from abc import ABC, abstractmethod
from typing import Any


class BaseTool(ABC):
    """Base class for agent tools."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Tool name for LLM."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Tool description for LLM."""
        pass

    @property
    @abstractmethod
    def parameters(self) -> dict[str, Any]:
        """JSON Schema for tool parameters."""
        pass

    @abstractmethod
    def execute(self, **kwargs: Any) -> str:
        """Execute the tool and return result as string."""
        pass
