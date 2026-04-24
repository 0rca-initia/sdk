import os
import sys
import json
import asyncio
import argparse
from typing import Dict, Any
from orca_dojo_sdk.wallet import DojoWallet
from orca_dojo_sdk.types import Task, TaskResult, LaneType, AgentConfig

# Mock concrete implementations for now
class ConcreteAgent:
    def __init__(self, config: Dict[str, Any], wallet: DojoWallet):
        self.config = config
        self.wallet = wallet

    async def process_task(self, task: Task) -> TaskResult:
        # Simulate AI processing
        print(f"DEBUG: Processing task {task.task_id} in lane {task.lane}")
        await asyncio.sleep(2)
        
        return TaskResult(
            task_id=task.task_id,
            success=True,
            output={"result": f"Completed {task.lane} task: {task.task_id}"},
            provenance_hash="KITE_MOCK_PROOF_123"
        )

class DojoAgentRunner:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.config_raw = self._load_config()
        self.wallet = DojoWallet(private_key=self.config_raw.get("private_key"))
        # Using a simple concrete agent for demo
        self.agent = ConcreteAgent(self.config_raw, self.wallet)

    def _load_config(self):
        config_str = os.getenv("DOJO_AGENT_CONFIG", "{}")
        try:
            return json.loads(config_str)
        except json.JSONDecodeError:
            return {}

    async def run(self):
        # Notify backend that agent is ready
        print(json.dumps({"type": "READY", "agentId": self.agent_id}))
        sys.stdout.flush()
        
        while True:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break
                
            try:
                msg = json.loads(line)
                if msg["type"] == "TASK_ASSIGN":
                    await self.handle_task(msg["taskId"], msg["payload"])
            except Exception as e:
                print(json.dumps({"type": "ERROR", "message": str(e)}))
                sys.stdout.flush()

    async def handle_task(self, task_id: str, payload: dict):
        # Map payload to Task type
        task = Task(
            task_id=task_id,
            lane=payload.get("lane", LaneType.RESEARCH),
            payload=payload,
            reward_micro_usdc=int(payload.get("bountyUsdc", 0))
        )
        
        try:
            result = await self.agent.process_task(task)
            print(json.dumps({
                "type": "TASK_COMPLETE",
                "taskId": task_id,
                "result": json.dumps(result.output),
                "provenanceHash": result.provenance_hash
            }))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({
                "type": "TASK_FAILED",
                "taskId": task_id,
                "message": str(e)
            }))
            sys.stdout.flush()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-id", required=True)
    args = parser.parse_args()
    
    runner = DojoAgentRunner(args.agent_id)
    asyncio.run(runner.run())
