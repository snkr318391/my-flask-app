import feedparser
import requests
from flask import Flask, render_template

app = Flask(__name__)

# List of subreddits and websites to fetch top posts from
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
    "thenation": "https://www.thenation.com/feed/?post_type=article&subject=politics",  # Updated RSS feed
    "muslimskeptic": "https://muslimskeptic.com/feed/",
    "theintercept": "https://theintercept.com/feed/",
    "slashdot": "http://rss.slashdot.org/Slashdot/slashdotMain",
    "aljazeera": "https://www.aljazeera.com/xml/rss/all.xml"
}

# Function to fetch posts from the RSS feed
def fetch_posts(feed_url):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    
    response = session.get(feed_url)
    
    # Parse the RSS feed
    feed = feedparser.parse(response.content)
    
    posts = []
    for entry in feed.entries[:5]:  # Display the first 5 headlines
        title = entry.title
        link = entry.link
        posts.append({"title": title, "link": link})

    return posts

# HTML Template for rendering posts
def generate_html(subreddit_posts):
    html_content = """
    <html>
    <head>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #000000;  /* Black background */
                color: #ffffff;  /* White text */
                text-align: center;
                margin: 0;
                padding: 20px;
            }
            .container {
                background-color: #1e1e1e;  /* Dark gray container */
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
                width: 80%;
                max-width: 800px;
                margin: 0 auto;
            }
            h1 {
                font-size: 2em;
                margin-bottom: 20px;
            }
            h2 {
                font-size: 1.5em;
                margin-top: 20px;
                color: #ffcc00;  /* Yellow for subreddit titles */
            }
            .post {
                margin: 10px 0;
                font-size: 1.1em;
            }
            a {
                color: #00FF00;  /* Green links */
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Top Posts of the Week</h1>
            """

    # Loop through each subreddit/website and add its posts
    for subreddit_or_site, posts in subreddit_posts.items():
        html_content += f"<h2>{subreddit_or_site}</h2>"
        for post in posts:
            html_content += f'<div class="post"><a href="{post["link"]}" target="_blank">{post["title"]}</a></div>'

    html_content += """
        </div>
    </body>
    </html>
    """
    return html_content

@app.route('/')
def index():
    subreddit_posts = {}

    # Fetch top posts from each subreddit or website
    for name, feed_url in subreddits_and_sites.items():
        posts = fetch_posts(feed_url)
        subreddit_posts[name] = posts

    # Check if any posts were fetched
    if not any(subreddit_posts.values()):
        return "No posts found. Reddit or websites may be blocking the request."

    # Generate and return the HTML content
    html_content = generate_html(subreddit_posts)
    return html_content

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
