from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from orca_dojo_sdk.lanes.base import BaseLane
from orca_dojo_sdk.types import LaneType


class OutreachLane(BaseLane, ABC):
    """Abstract base class for agents specialized in communication or CRM."""

    def __init__(self):
        super().__init__(LaneType.OUTREACH)

    @abstractmethod
    async def draft_communication(self, recipient: str, message_intent: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Base method for outreach task execution.
        
        Args:
            recipient: The target of the outreach.
            message_intent: The purpose of the message.
            context: Additional details for communication.
        
        Returns:
            The drafted communication message.
        """
        pass
