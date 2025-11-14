"""
Configuration management for Reddit API Client.
Loads credentials and settings from environment variables.
"""

import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class Config:
    """
    Reddit API configuration.

    Attributes:
        client_id: Reddit application client ID
        client_secret: Reddit application client secret
        user_agent: User agent string for API requests
        username: Reddit username (optional, for user-specific operations)
        password: Reddit password (optional, for user-specific operations)
    """
    client_id: str
    client_secret: str
    user_agent: str
    username: Optional[str] = None
    password: Optional[str] = None

    @classmethod
    def from_env(cls, env_file: str = ".env") -> "Config":
        """
        Load configuration from environment variables.

        Args:
            env_file: Path to .env file (default: ".env")

        Returns:
            Config instance with loaded settings

        Raises:
            ValueError: If required environment variables are missing
        """
        # Load environment variables from .env file
        load_dotenv(env_file)

        # Required credentials
        client_id = os.getenv("REDDIT_CLIENT_ID")
        client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        user_agent = os.getenv("REDDIT_USER_AGENT", "reddit-api-client/1.0")

        if not client_id or not client_secret:
            raise ValueError(
                "Missing required environment variables: "
                "REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET must be set"
            )

        # Optional credentials for authenticated requests
        username = os.getenv("REDDIT_USERNAME")
        password = os.getenv("REDDIT_PASSWORD")

        return cls(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
            username=username,
            password=password
        )

    def is_authenticated(self) -> bool:
        """Check if username and password are provided for authenticated access."""
        return bool(self.username and self.password)
