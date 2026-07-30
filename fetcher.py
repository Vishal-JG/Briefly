import os
import feedparser
from urllib.parse import urlparse

def get_feeds():
    feeds_env = os.environ.get("FEEDS", "")
    return [f.strip() for f in feeds_env.split(",") if f.strip()]

def fetch_all_feeds():
    articles = []
    for url in get_feeds():
        parsed = feedparser.parse(url)
        domain = urlparse(url).netloc.replace("www.", "")
        for entry in parsed.entries:
            articles.append({
                "title": entry.get("title", ""),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "source": domain
            })
    return articles