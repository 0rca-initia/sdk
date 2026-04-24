from enum import Enum
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class LaneType(str, Enum):
    """Supported 0rca Dojo lanes."""
    RESEARCH = "research"
    CODE = "code"
    DATA = "data"
    OUTREACH = "outreach"


class AgentConfig(BaseModel):
    """Configuration for a Dojo agent."""
    agent_id: str = Field(..., alias="agent_address", description="Unique ID for the agent")
    lane: LaneType = Field(..., description="Agent specialization")
    llmTier: str = Field(..., description="LLM capability tier")
    biddingStrategy: str = Field(..., description="Bidding behavior policy")
    openai_api_key: str = Field(..., description="Sensei's OpenAI API Key")
    llm_params: Optional[Dict[str, Any]] = Field(default=None, description="Resolved LLM parameters (model, cost, etc.)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Custom agent metadata")

    class Config:
        populate_by_name = True
        extra = "allow"


class Task(BaseModel):
    """Represents a task assigned to an agent."""
    task_id: str = Field(..., description="Unique task identifier")
    lane: LaneType = Field(..., description="Required lane for task")
    payload: Dict[str, Any] = Field(..., description="Input data for the task")
    deadline: Optional[int] = Field(None, description="UNIX timestamp deadline")
    reward_micro_usdc: int = Field(..., description="Reward in microUSDC")


class TaskResult(BaseModel):
    """Represents the output from a completed task."""
    task_id: str = Field(..., description="Associated task ID")
    success: bool = Field(..., description="Whether task was completed successfully")
    output: Dict[str, Any] = Field(..., description="Result payload")
    provenance_hash: Optional[str] = Field(None, description="Kite AI provenance proof")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Execution metrics/logs")
