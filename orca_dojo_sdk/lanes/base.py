from abc import ABC, abstractmethod
from typing import Any, Dict
from orca_dojo_sdk.agent import BaseAgent
from orca_dojo_sdk.types import LaneType


class BaseLane(BaseAgent, ABC):
    """Abstract base class for all 0rca Dojo lane specializations."""

    def __init__(self, lane_type: LaneType, config: AgentConfig, wallet: Optional[DojoWallet] = None):
        """
        Initializes the lane with its type and agent configuration.
        
        Args:
            lane_type: The specialization of this lane.
            config: The agent's unique configuration.
            wallet: The agent's Initia wallet.
        """
        super().__init__(config, wallet)
        self.lane_type = lane_type

    @abstractmethod
    def validate_task_payload(self, payload: Dict[str, Any]) -> bool:
        """
        Validates the task data for its specific lane format.
        
        Args:
            payload: The task data dictionary.
        
        Returns:
            True if valid, False otherwise.
        """
        pass
