import feedparser
from urllib.parse import urlparse


FEEDS = [
    "http://feeds.bbci.co.uk/news/world/rss.xml",
    "https://techcrunch.com/feed/",
    "https://www.straitstimes.com/rss.xml",
    "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "https://www.abc.net.au/news/feed/51120/rss.xml",
    "https://feeds.reuters.com/reuters/topNews",
]

def fetch_all_feeds():
    articles = []
    for url in FEEDS:
        parsed = feedparser.parse(url)
        domain = urlparse(url).netloc.replace("www.", "")
        for entry in parsed.entries:
            articles.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", ""),
                "source": domain
            })
    return articles