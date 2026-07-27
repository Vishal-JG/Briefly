SOURCE_WEIGHTS = {
    "reuters.com": 10, "apnews.com": 10, "bbc.com": 9,
    "techcrunch.com": 7, "straitstimes.com": 8, "default": 3
}

KEYWORDS = ["AI", "cloud", "election", "policy", "cybersecurity"]

def recency_score(published_dt, now):
    hours_old = (now - published_dt).total_seconds() / 3600
    if hours_old <= 6: return 5
    if hours_old <= 12: return 3
    if hours_old <= 24: return 1
    return 0

def keyword_score(title):
    return sum(2 for kw in KEYWORDS if kw.lower() in title.lower())

def score_article(article, mention_count):
    from datetime import datetime
    from dateutil import parser as date_parser

    domain = article.get("source", "default")
    title = article.get("title", "")
    published_raw = article.get("published", "")

    try:
        published_dt = date_parser.parse(published_raw)
        now = datetime.now(published_dt.tzinfo)
        rec_score = recency_score(published_dt, now)
    except Exception:
        rec_score = 0

    return (
        SOURCE_WEIGHTS.get(domain, SOURCE_WEIGHTS["default"])
        + rec_score
        + keyword_score(title)
        + mention_count * 2
    )