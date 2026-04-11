
from abc import ABC, abstractmethod
from typing import Any, Dict

from src.workflow.state import FinanceAssistantState


class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def run(self, state: FinanceAssistantState) -> FinanceAssistantState:
        """Run agent logic and return updated shared state."""
        raise NotImplementedError