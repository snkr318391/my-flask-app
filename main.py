import feedparser
import requests
from flask import Flask
import time
import logging

app = Flask(__name__)

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of subreddits and websites
subreddits_and_sites = {
    "technology": "https://www.reddit.com/r/technology/top/.rss?t=week",
    "nba": "https://www.reddit.com/r/nba/top/.rss?t=week",
    "news": "https://www.reddit.com/r/news/top/.rss?t=week",
    "unusual_whales": "https://www.reddit.com/r/unusual_whales/top/.rss?t=week",
    "PanIslamistPosting": "https://www.reddit.com/r/PanIslamistPosting/top/.rss?t=week",
    "Futurology": "https://www.reddit.com/r/Futurology/top/.rss?t=week",
    "geopolitics": "https://www.reddit.com/r/geopolitics/top/.rss?t=week",
    "bestof": "https://www.reddit.com/r/bestof/top/.rss?t=week",
    "truereddit": "https://www.reddit.com/r/truereddit/top/.rss?t=week",
    "thenation": "https://www.thenation.com/feed/?post_type=article&subject=politics",
    "muslimskeptic": "https://muslimskeptic.com/feed/",
    "theintercept": "https://theintercept.com/feed/",
    "slashdot": "http://rss.slashdot.org/Slashdot/slashdotMain",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml"
}

# Cache dictionary
cache = {"data": {}, "last_updated": 0}
CACHE_DURATION = 3600  # 1 hour in seconds

# Function to fetch posts
def fetch_posts(feed_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        logger.info(f"Fetching posts from {feed_url}")
        response = requests.get(feed_url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching {feed_url}: {e}")
        return []

    feed = feedparser.parse(response.content)
    return [{"title": entry.title, "link": entry.link} for entry in feed.entries[:5]]

# Function to update cache
def update_cache():
    global cache
    if time.time() - cache["last_updated"] < CACHE_DURATION:
        logger.info("Using cached data")
        return cache["data"]

    logger.info("Updating cache with fresh data")
    subreddit_posts = {name: fetch_posts(url) for name, url in subreddits_and_sites.items()}
    cache = {"data": subreddit_posts, "last_updated": time.time()}
    return subreddit_posts

@app.route('/')
def index():
    subreddit_posts = update_cache()
    
    # Generate HTML output
    html_content = "<html><head><style>body{font-family:Arial;background:#000;color:#fff;text-align:center;padding:20px} .container{background:#1e1e1e;padding:20px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.5);width:80%;max-width:800px;margin:0 auto} h1{font-size:2em;margin-bottom:20px} h2{font-size:1.5em;margin-top:20px;color:#ffcc00} .post{margin:10px 0;font-size:1.1em} a{color:#00FF00;text-decoration:none} a:hover{text-decoration:underline}</style></head><body><div class='container'><h1>Top Posts of the Week</h1>"

    for subreddit, posts in subreddit_posts.items():
        if posts:
            html_content += f"<h2>{subreddit.capitalize()}</h2>"
            for post in posts:
                html_content += f'<div class="post"><a href="{post["link"]}" target="_blank">{post["title"]}</a></div>'

    html_content += "</div></body></html>"
    return html_content
