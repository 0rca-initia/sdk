from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from orca_dojo_sdk.lanes.base import BaseLane
from orca_dojo_sdk.types import LaneType


class CodeLane(BaseLane, ABC):
    """Abstract base class for agents specialized in code generation or review."""

    def __init__(self):
        super().__init__(LaneType.CODE)

    @abstractmethod
    async def generate_code(self, prompt: str, language: str) -> str:
        """
        Base method for code generation task execution.
        
        Args:
            prompt: The coding prompt or instruction.
            language: Target programming language.
        
        Returns:
            The generated code string.
        """
        pass
