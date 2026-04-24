import os
from typing import Optional, Union
import algosdk
from algosdk import account, mnemonic, transaction


class DojoWallet:
    """Wrapper for Algorand agent wallet operations."""

    def __init__(self, private_key: Optional[str] = None, seed_phrase: Optional[str] = None):
        """
        Initializes a DojoWallet with a private key or mnemonic phrase.
        
        Args:
            private_key: Hex string representation of the Algorand private key.
            seed_phrase: 25-word Algorand mnemonic phrase.
        """
        if seed_phrase:
            self.private_key = mnemonic.to_private_key(seed_phrase)
        elif private_key:
            self.private_key = private_key
        else:
            # Fallback to environment variable or raise error
            env_key = os.getenv("DOJO_AGENT_PRIVATE_KEY")
            if env_key:
                self.private_key = env_key
            else:
                raise ValueError("DojoWallet must be initialized with a private key or mnemonic.")

        self.address = account.address_from_private_key(self.private_key)

    @classmethod
    def create_random(cls) -> 'DojoWallet':
        """Generates a new random Algorand wallet."""
        priv_key, _ = account.generate_account()
        return cls(private_key=priv_key)

    def sign_transaction(self, txn: transaction.Transaction) -> transaction.SignedTransaction:
        """Signs an Algorand transaction with the wallet's private key."""
        return txn.sign(self.private_key)

    def get_public_address(self) -> str:
        """Returns the Algorand public address of the wallet."""
        return self.address

    def get_mnemonic(self) -> str:
        """Returns the 25-word mnemonic phrase for the wallet."""
        return mnemonic.from_private_key(self.private_key)
