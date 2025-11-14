"""
Example: Calculate statistics for a subreddit.

This script demonstrates how to fetch and calculate basic statistics
for a subreddit using the Reddit API Client.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path to import reddit_client
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from reddit_client import RedditClient, Config


def main():
    """Calculate and display subreddit statistics."""
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

    # Get subreddit to analyze
    subreddit_name = input("Enter subreddit name (without r/): ").strip() or "python"
    limit = 100

    print(f"\nAnalyzing r/{subreddit_name} (analyzing {limit} hot posts)...\n")

    try:
        # Get subreddit info
        info = client.get_subreddit_info(subreddit_name)
        print("Subreddit Information:")
        print(f"  Title: {info['title']}")
        print(f"  Subscribers: {info['subscribers']:,}")
        print(f"  Active Users: {info['active_users']:,}")
        print(f"  Created: {info['created_utc']}")
        print(f"  NSFW: {info['is_over18']}")
        print(f"  URL: {info['url']}")
        print()

        # Get statistics
        stats = client.get_subreddit_stats(subreddit_name, limit=limit)
        print("Post Statistics (based on hot posts):")
        print(f"  Total Posts Analyzed: {stats['total_posts']}")
        print(f"  Total Score: {stats['total_score']:,}")
        print(f"  Total Comments: {stats['total_comments']:,}")
        print(f"  Average Score per Post: {stats['average_score']:.2f}")
        print(f"  Average Comments per Post: {stats['average_comments']:.2f}")
        print(f"  Analysis Time: {stats['analyzed_time']}")
        print()

        # Combine info and stats
        result = {
            "subreddit_info": info,
            "statistics": stats
        }

        # Save to JSON file
        output_file = f"{subreddit_name}_stats.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"Results saved to {output_file}")

    except Exception as e:
        print(f"Error analyzing subreddit: {e}")


if __name__ == "__main__":
    main()
