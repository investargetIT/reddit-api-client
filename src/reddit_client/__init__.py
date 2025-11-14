"""
Reddit API Client - A read-only client for accessing public subreddit data.
"""

from .api_client import RedditClient
from .config import Config

__version__ = "1.0.0"
__all__ = ["RedditClient", "Config"]
