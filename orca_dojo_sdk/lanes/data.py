from abc import ABC, abstractmethod
from typing import Dict, Any, List
from orca_dojo_sdk.lanes.base import BaseLane
from orca_dojo_sdk.types import LaneType


class DataLane(BaseLane, ABC):
    """Abstract base class for agents specialized in dataset curation or analysis."""

    def __init__(self):
        super().__init__(LaneType.DATA)

    @abstractmethod
    async def process_dataset(self, data: List[Dict[str, Any]], transformation: str) -> List[Dict[str, Any]]:
        """
        Base method for data processing task execution.
        
        Args:
            data: The input dataset.
            transformation: The instruction for data manipulation.
        
        Returns:
            The transformed dataset.
        """
        pass
