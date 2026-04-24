from abc import ABC, abstractmethod
from typing import Optional, Any
from orca_dojo_sdk.types import AgentConfig, Task, TaskResult
from orca_dojo_sdk.wallet import DojoWallet


class BaseAgent(ABC):
    """Abstract base class for all 0rca Dojo agents."""

    def __init__(self, config: Any, wallet: Optional[DojoWallet] = None):
        """
        Initializes the agent with configuration and optional wallet.
        
        Args:
            config: The agent's unique configuration.
            wallet: The agent's Initia wallet for transaction signing.
        """
        self.config = config
        self.wallet = wallet or DojoWallet.create_random()
        self.is_active = False

        # Validate API key is present in config (OpenAI sk- or Groq gsk_)
        api_key = self.config.get("openai_api_key", "")
        if not api_key or not (api_key.startswith("sk-") or api_key.startswith("gsk_")):
            raise ValueError(
                f"Agent {self.config.get('agent_address', 'unknown')} "
                f"has no valid openai_api_key in its sealed config. "
                f"The Sensei must re-register this agent and provide "
                f"a valid OpenAI API key."
            )

        # Validate llm_params were resolved by config_loader
        if "llm_params" not in self.config:
            raise ValueError(
                f"Agent {self.config.get('agent_address', 'unknown')} "
                f"config is missing llm_params. "
                f"This means config_loader did not resolve the LLM tier. "
                f"Check config_loader.py LLM_TIER_MAP logic."
            )

    def get_llm_params(self) -> dict:
        return self.config["llm_params"]

    def get_openai_key(self) -> str:
        return self.config["openai_api_key"]

    def activate(self):
        """Starts the agent's listener/execution cycle."""
        self.is_active = True
        self.on_activated()

    def deactivate(self):
        """Stops the agent's lifecycle."""
        self.is_active = False
        self.on_deactivated()

    @abstractmethod
    async def process_task(self, task: Task) -> TaskResult:
        """
        Core task execution logic to be implemented by concrete agents.
        
        Args:
            task: The assigned task payload.
        
        Returns:
            TaskResult containing the execution outcome and metadata.
        """
        pass

    def on_activated(self):
        """Hook called when the agent starts."""
        pass

    def on_deactivated(self):
        """Hook called when the agent stops."""
        pass

    def on_task_received(self, task: Task):
        """Hook called when a new task is detected."""
        pass

    def on_task_completed(self, result: TaskResult):
        """Hook called after task processing is finished."""
        pass
