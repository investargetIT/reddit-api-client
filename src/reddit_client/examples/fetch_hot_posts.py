"""
Example: Fetch hot posts from a subreddit.

This script demonstrates how to fetch and display hot posts from
a specified subreddit using the Reddit API Client.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path to import reddit_client
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from reddit_client import RedditClient, Config


def main():
    """Fetch and display hot posts from a subreddit."""
    # Load configuration from environment
    try:
        config = Config.from_env()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nPlease ensure you have a .env file with the following variables:")
        print("  REDDIT_CLIENT_ID=your_client_id")
        print("  REDDIT_CLIENT_SECRET=your_client_secret")
        print("  REDDIT_USER_AGENT=reddit-api-client/1.0")
        return

    # Initialize client
    client = RedditClient(config)

    # Fetch hot posts from r/python
    subreddit_name = "python"
    limit = 10

    print(f"\nFetching top {limit} hot posts from r/{subreddit_name}...\n")

    try:
        posts = client.get_hot_posts(subreddit_name, limit=limit)

        # Display posts
        for i, post in enumerate(posts, 1):
            print(f"{i}. {post['title']}")
            print(f"   Author: {post['author']}")
            print(f"   Score: {post['score']} | Comments: {post['num_comments']}")
            print(f"   URL: {post['permalink']}")
            print()

        # Optionally save to JSON file
        output_file = f"{subreddit_name}_hot_posts.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)

        print(f"Results saved to {output_file}")

    except Exception as e:
        print(f"Error fetching posts: {e}")


if __name__ == "__main__":
    main()
