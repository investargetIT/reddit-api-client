"""
Reddit API Client - A thin wrapper around PRAW for read-only access.
"""

import praw
from typing import List, Dict, Any, Optional
from datetime import datetime
from .config import Config


class RedditClient:
    """
    A read-only client for accessing Reddit's public data.

    This client provides methods to fetch posts, comments, and basic
    statistics from public subreddits. All operations are read-only.
    """

    def __init__(self, config: Config):
        """
        Initialize the Reddit client.

        Args:
            config: Configuration object with Reddit API credentials
        """
        self.config = config

        # Initialize PRAW Reddit instance
        if config.is_authenticated():
            self.reddit = praw.Reddit(
                client_id=config.client_id,
                client_secret=config.client_secret,
                user_agent=config.user_agent,
                username=config.username,
                password=config.password
            )
        else:
            # Read-only mode (no username/password)
            self.reddit = praw.Reddit(
                client_id=config.client_id,
                client_secret=config.client_secret,
                user_agent=config.user_agent
            )

        # Set read-only mode
        self.reddit.read_only = True

    def get_hot_posts(
        self,
        subreddit_name: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fetch hot posts from a subreddit.

        Args:
            subreddit_name: Name of the subreddit (without 'r/')
            limit: Maximum number of posts to fetch (default: 10)

        Returns:
            List of dictionaries containing post data

        Example:
            >>> client = RedditClient(config)
            >>> posts = client.get_hot_posts("python", limit=5)
        """
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []

        for submission in subreddit.hot(limit=limit):
            posts.append(self._format_submission(submission))

        return posts

    def get_new_posts(
        self,
        subreddit_name: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fetch newest posts from a subreddit.

        Args:
            subreddit_name: Name of the subreddit (without 'r/')
            limit: Maximum number of posts to fetch (default: 10)

        Returns:
            List of dictionaries containing post data
        """
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []

        for submission in subreddit.new(limit=limit):
            posts.append(self._format_submission(submission))

        return posts

    def get_top_posts(
        self,
        subreddit_name: str,
        time_filter: str = "day",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Fetch top posts from a subreddit.

        Args:
            subreddit_name: Name of the subreddit (without 'r/')
            time_filter: Time period filter ("hour", "day", "week", "month", "year", "all")
            limit: Maximum number of posts to fetch (default: 10)

        Returns:
            List of dictionaries containing post data
        """
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []

        for submission in subreddit.top(time_filter=time_filter, limit=limit):
            posts.append(self._format_submission(submission))

        return posts

    def search_posts(
        self,
        subreddit_name: str,
        query: str,
        sort: str = "relevance",
        time_filter: str = "all",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Search for posts in a subreddit.

        Args:
            subreddit_name: Name of the subreddit (without 'r/')
            query: Search query string
            sort: Sort method ("relevance", "hot", "top", "new", "comments")
            time_filter: Time period filter ("hour", "day", "week", "month", "year", "all")
            limit: Maximum number of posts to fetch (default: 10)

        Returns:
            List of dictionaries containing post data
        """
        subreddit = self.reddit.subreddit(subreddit_name)
        posts = []

        for submission in subreddit.search(query, sort=sort, time_filter=time_filter, limit=limit):
            posts.append(self._format_submission(submission))

        return posts

    def get_post_comments(
        self,
        post_id: str,
        limit: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch comments from a specific post.

        Args:
            post_id: Reddit post ID
            limit: Maximum number of comments to fetch (None for all)

        Returns:
            List of dictionaries containing comment data
        """
        submission = self.reddit.submission(id=post_id)

        # Replace MoreComments objects with actual comments
        if limit:
            submission.comments.replace_more(limit=0)

        comments = []
        for comment in submission.comments.list():
            if hasattr(comment, 'body'):  # Skip MoreComments objects
                comments.append(self._format_comment(comment))
                if limit and len(comments) >= limit:
                    break

        return comments

    def get_subreddit_info(self, subreddit_name: str) -> Dict[str, Any]:
        """
        Get information about a subreddit.

        Args:
            subreddit_name: Name of the subreddit (without 'r/')

        Returns:
            Dictionary containing subreddit information
        """
        subreddit = self.reddit.subreddit(subreddit_name)

        return {
            "name": subreddit.display_name,
            "title": subreddit.title,
            "description": subreddit.public_description,
            "subscribers": subreddit.subscribers,
            "active_users": subreddit.active_user_count,
            "created_utc": datetime.fromtimestamp(subreddit.created_utc).isoformat(),
            "is_over18": subreddit.over18,
            "url": f"https://reddit.com{subreddit.url}"
        }

    def get_subreddit_stats(self, subreddit_name: str, limit: int = 100) -> Dict[str, Any]:
        """
        Calculate basic statistics for a subreddit based on hot posts.

        Args:
            subreddit_name: Name of the subreddit (without 'r/')
            limit: Number of posts to analyze (default: 100)

        Returns:
            Dictionary containing statistics
        """
        posts = self.get_hot_posts(subreddit_name, limit=limit)

        if not posts:
            return {
                "total_posts": 0,
                "total_score": 0,
                "total_comments": 0,
                "average_score": 0,
                "average_comments": 0
            }

        total_score = sum(post["score"] for post in posts)
        total_comments = sum(post["num_comments"] for post in posts)

        return {
            "total_posts": len(posts),
            "total_score": total_score,
            "total_comments": total_comments,
            "average_score": total_score / len(posts),
            "average_comments": total_comments / len(posts),
            "analyzed_time": datetime.now().isoformat()
        }

    def _format_submission(self, submission) -> Dict[str, Any]:
        """
        Format a PRAW submission object into a dictionary.

        Args:
            submission: PRAW Submission object

        Returns:
            Dictionary with formatted submission data
        """
        return {
            "id": submission.id,
            "title": submission.title,
            "author": str(submission.author) if submission.author else "[deleted]",
            "score": submission.score,
            "upvote_ratio": submission.upvote_ratio,
            "num_comments": submission.num_comments,
            "created_utc": datetime.fromtimestamp(submission.created_utc).isoformat(),
            "url": submission.url,
            "permalink": f"https://reddit.com{submission.permalink}",
            "is_self": submission.is_self,
            "selftext": submission.selftext if submission.is_self else None,
            "link_flair_text": submission.link_flair_text,
            "subreddit": str(submission.subreddit),
            "is_over18": submission.over_18,
            "spoiler": submission.spoiler,
            "stickied": submission.stickied
        }

    def _format_comment(self, comment) -> Dict[str, Any]:
        """
        Format a PRAW comment object into a dictionary.

        Args:
            comment: PRAW Comment object

        Returns:
            Dictionary with formatted comment data
        """
        return {
            "id": comment.id,
            "author": str(comment.author) if comment.author else "[deleted]",
            "body": comment.body,
            "score": comment.score,
            "created_utc": datetime.fromtimestamp(comment.created_utc).isoformat(),
            "permalink": f"https://reddit.com{comment.permalink}",
            "is_submitter": comment.is_submitter,
            "parent_id": comment.parent_id,
            "depth": comment.depth
        }
