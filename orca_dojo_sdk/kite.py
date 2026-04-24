from typing import Dict, Any, Optional
import httpx
from orca_dojo_sdk.types import TaskResult


class KiteClient:
    """Client for interacting with the Kite AI provenance API."""

    def __init__(self, api_key: str, base_url: str = "https://api.kite.ai/v1"):
        """
        Initializes the Kite AI client.
        
        Args:
            api_key: Your Kite AI authentication key.
            base_url: The API endpoint for Kite AI.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def submit_provenance(self, result: TaskResult) -> str:
        """
        Submits a task result to Kite AI for provenance tracking.
        
        Args:
            result: The completed task result.
        
        Returns:
            The provenance hash (proof) provided by Kite AI.
        """
        async with httpx.AsyncClient() as client:
            payload = {
                "task_id": result.task_id,
                "output_summary": str(result.output)[:1000],  # Truncate for summary
                "metadata": result.metadata
            }
            
            response = await client.post(
                f"{self.base_url}/provenance",
                json=payload,
                headers=self.headers
            )
            
            response.raise_for_status()
            data = response.json()
            return data.get("provenance_hash", "pending")

    async def verify_proof(self, provenance_hash: str) -> bool:
        """
        Verifies a previously generated provenance proof.
        
        Args:
            provenance_hash: The hash to verify.
        
        Returns:
            True if valid, False otherwise.
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/verify/{provenance_hash}",
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json().get("valid", False)
            return False
