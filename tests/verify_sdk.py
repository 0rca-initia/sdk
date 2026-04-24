import sys
import os

# Add current directory to sys.path if not installed
sys.path.append(os.getcwd())

from orca_dojo_sdk import DojoWallet, AgentConfig, Task, LaneType
from orca_dojo_sdk.lanes import ResearchLane

def test_wallet():
    print("Testing DojoWallet...")
    wallet = DojoWallet.create_random()
    print(f"Address: {wallet.get_public_address()}")
    assert len(wallet.get_public_address()) == 58
    print("Wallet OK.")

def test_types():
    print("Testing Pydantic Types...")
    config = AgentConfig(
        agent_id="test-agent-001",
        lane=LaneType.RESEARCH,
        llm_tier="high",
        bidding_strategy="aggressive"
    )
    print(f"Config: {config.model_dump()}")
    
    task = Task(
        task_id="task-123",
        lane=LaneType.RESEARCH,
        payload={"query": "Who is 0rca?"},
        reward_micro_usdc=1000000
    )
    print(f"Task: {task.model_dump()}")
    print("Types OK.")

if __name__ == "__main__":
    try:
        test_wallet()
        test_types()
        print("\nAll SDK local verifications PASSED.")
    except Exception as e:
        print(f"\nVerification FAILED: {e}")
        sys.exit(1)
