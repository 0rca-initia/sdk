from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from orca_dojo_sdk.lanes.base import BaseLane
from orca_dojo_sdk.wallet import DojoWallet
from orca_dojo_sdk.agent import BaseAgent
from orca_dojo_sdk.types import LaneType, AgentConfig


class ResearchLane(BaseLane, ABC):
    """Abstract base class for agents specialized in research."""

    def __init__(self, config: AgentConfig, wallet: Optional[DojoWallet] = None):
        super().__init__(LaneType.RESEARCH, config, wallet)

    @abstractmethod
    async def perform_research(self, query: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Base method for research task execution.
        
        Args:
            query: The research question or query.
            context: Additional constraints or data.
        
        Returns:
            The synthesized research result.
        """
        pass
