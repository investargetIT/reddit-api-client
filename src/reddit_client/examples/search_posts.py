"""
Example: Search for posts in a subreddit.

This script demonstrates how to search for posts matching a query
in a specific subreddit.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path to import reddit_client
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from reddit_client import RedditClient, Config


def main():
    """Search for posts in a subreddit."""
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

    # Get search parameters
    subreddit_name = input("Enter subreddit name (without r/): ").strip() or "python"
    query = input("Enter search query: ").strip() or "machine learning"
    limit = 20

    print(f"\nSearching r/{subreddit_name} for '{query}'...\n")

    try:
        # Search posts
        posts = client.search_posts(
            subreddit_name=subreddit_name,
            query=query,
            sort="relevance",
            time_filter="all",
            limit=limit
        )

        if not posts:
            print("No posts found matching your query.")
            return

        # Display posts
        for i, post in enumerate(posts, 1):
            print(f"{i}. {post['title']}")
            print(f"   Author: {post['author']}")
            print(f"   Score: {post['score']} | Comments: {post['num_comments']}")
            print(f"   Created: {post['created_utc']}")
            print(f"   URL: {post['permalink']}")
            print()

        # Save to JSON file
        output_file = f"{subreddit_name}_search_{query.replace(' ', '_')}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)

        print(f"Results saved to {output_file}")

    except Exception as e:
        print(f"Error searching posts: {e}")


if __name__ == "__main__":
    main()
