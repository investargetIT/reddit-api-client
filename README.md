# Reddit API Client

A read-only Python client for accessing public subreddit data via the official Reddit API. This project demonstrates how to integrate with Reddit in a compliant and transparent way for analytics and insights.

## Features

- **Read-only access** to public subreddit posts via Reddit's official API
- **Simple wrapper** around [PRAW](https://praw.readthedocs.io/) for common tasks
- **Multiple data access methods**:
  - Fetch hot, new, and top posts from any subreddit
  - Search posts by keywords
  - Retrieve post comments
  - Calculate subreddit statistics
  - Get subreddit information
- **Configurable API credentials** via environment variables
- **Example scripts** demonstrating common use cases

All API usage respects Reddit's API policies and rate limits.

---

## Project Structure

```
reddit-api-client/
├── src/
│   └── reddit_client/
│       ├── __init__.py           # Package initialization
│       ├── config.py              # API configuration management
│       ├── api_client.py          # Main Reddit API client wrapper
│       └── examples/
│           ├── __init__.py
│           ├── fetch_hot_posts.py        # Example: Fetch hot posts
│           ├── fetch_subreddit_stats.py  # Example: Calculate subreddit stats
│           └── search_posts.py           # Example: Search posts by query
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore patterns
├── LICENSE                        # MIT License
└── README.md                      # This file
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/investargetIT/reddit-api-client.git
cd reddit-api-client
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Reddit API Credentials

#### Step 1: Create a Reddit Application

1. Go to https://www.reddit.com/prefs/apps
2. Click "Create App" or "Create Another App"
3. Fill in the form:
   - **name**: reddit-api-client (or your preferred name)
   - **App type**: Select "script"
   - **description**: Read-only client for analytics (optional)
   - **about url**: Leave blank (optional)
   - **redirect uri**: http://localhost:8080 (required but not used)
4. Click "Create app"
5. Note your **client ID** (under the app name) and **client secret**

#### Step 2: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and fill in your credentials
# REDDIT_CLIENT_ID=your_client_id_here
# REDDIT_CLIENT_SECRET=your_client_secret_here
# REDDIT_USER_AGENT=reddit-api-client/1.0 (by /u/your_username)
```

**Important**: Never commit your `.env` file to version control. It's already included in `.gitignore`.

---

## Usage

### Quick Start

```python
from reddit_client import RedditClient, Config

# Load configuration from .env file
config = Config.from_env()

# Initialize the client
client = RedditClient(config)

# Fetch hot posts from r/python
posts = client.get_hot_posts("python", limit=10)

# Display posts
for post in posts:
    print(f"{post['title']} - Score: {post['score']}")
```

### API Methods

#### 1. Fetch Hot Posts

```python
posts = client.get_hot_posts("python", limit=10)
```

#### 2. Fetch New Posts

```python
posts = client.get_new_posts("python", limit=10)
```

#### 3. Fetch Top Posts

```python
# Time filters: "hour", "day", "week", "month", "year", "all"
posts = client.get_top_posts("python", time_filter="week", limit=10)
```

#### 4. Search Posts

```python
posts = client.search_posts(
    subreddit_name="python",
    query="machine learning",
    sort="relevance",
    time_filter="all",
    limit=20
)
```

#### 5. Get Post Comments

```python
comments = client.get_post_comments(post_id="abc123", limit=50)
```

#### 6. Get Subreddit Information

```python
info = client.get_subreddit_info("python")
print(f"Subscribers: {info['subscribers']}")
```

#### 7. Calculate Subreddit Statistics

```python
stats = client.get_subreddit_stats("python", limit=100)
print(f"Average score: {stats['average_score']}")
```

---

## Example Scripts

The `src/reddit_client/examples/` directory contains ready-to-run example scripts:

### 1. Fetch Hot Posts

```bash
cd src/reddit_client/examples
python fetch_hot_posts.py
```

Fetches the top 10 hot posts from r/python and saves them to a JSON file.

### 2. Calculate Subreddit Statistics

```bash
python fetch_subreddit_stats.py
```

Analyzes a subreddit and displays statistics (subscribers, average score, etc.).

### 3. Search Posts

```bash
python search_posts.py
```

Searches for posts matching a query in a specified subreddit.

---

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `REDDIT_CLIENT_ID` | Yes | Reddit application client ID |
| `REDDIT_CLIENT_SECRET` | Yes | Reddit application client secret |
| `REDDIT_USER_AGENT` | Yes | User agent string (format: `app:version (by /u/username)`) |
| `REDDIT_USERNAME` | No | Reddit username (for authenticated access, currently not used) |
| `REDDIT_PASSWORD` | No | Reddit password (for authenticated access, currently not used) |

### API Rate Limits

Reddit enforces rate limits on API requests:
- **OAuth requests**: 60 requests per minute
- **Script applications**: 10 requests per minute

The PRAW library automatically handles rate limiting and will sleep if necessary.

---

## Development

### Running Tests

```bash
# Install development dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run tests with coverage
pytest --cov=src/reddit_client
```

### Code Formatting

```bash
# Install black
pip install black

# Format code
black src/
```

### Type Checking

```bash
# Install mypy
pip install mypy

# Check types
mypy src/
```

---

## API Response Format

### Post Object

```json
{
  "id": "abc123",
  "title": "Example Post Title",
  "author": "username",
  "score": 1234,
  "upvote_ratio": 0.95,
  "num_comments": 56,
  "created_utc": "2024-01-01T12:00:00",
  "url": "https://example.com",
  "permalink": "https://reddit.com/r/python/comments/abc123/...",
  "is_self": true,
  "selftext": "Post content...",
  "link_flair_text": "Discussion",
  "subreddit": "python",
  "is_over18": false,
  "spoiler": false,
  "stickied": false
}
```

### Comment Object

```json
{
  "id": "def456",
  "author": "username",
  "body": "Comment text...",
  "score": 42,
  "created_utc": "2024-01-01T12:30:00",
  "permalink": "https://reddit.com/r/python/comments/abc123/.../def456",
  "is_submitter": false,
  "parent_id": "t3_abc123",
  "depth": 0
}
```

---

## Compliance & Privacy

- **Read-only**: This client only reads public data; it does not post, comment, vote, or modify any Reddit content
- **Public data**: Only accesses publicly available subreddit posts and comments
- **Rate limits**: Respects Reddit's API rate limits
- **User agent**: Identifies itself with a proper user agent string
- **No data storage**: Example scripts save data locally for demonstration only

---

## Troubleshooting

### Error: "Missing required environment variables"

Make sure you've created a `.env` file and filled in your Reddit API credentials.

### Error: "Received 401 HTTP response"

Your client ID or client secret is incorrect. Double-check your credentials in the `.env` file.

### Error: "Too Many Requests"

You've hit Reddit's rate limit. The PRAW library will automatically wait, but you can reduce your request frequency.

---

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Resources

- [PRAW Documentation](https://praw.readthedocs.io/)
- [Reddit API Documentation](https://www.reddit.com/dev/api/)
- [Reddit API Rules](https://github.com/reddit-archive/reddit/wiki/API)
- [How to create a Reddit app](https://www.reddit.com/wiki/api)

---

## Contact

For questions or issues, please open an issue on GitHub.

---

**Built with Python and PRAW**
