SOURCE_WEIGHTS = {
    "reuters.com": 10, "apnews.com": 10, "bbc.com": 9,
    "techcrunch.com": 7, "straitstimes.com": 8, "default": 3
}

def recency_score(published_dt, now):
    hours_old = (now - published_dt).total_seconds() / 3600
    if hours_old <= 6: return 5
    if hours_old <= 12: return 3
    if hours_old <= 24: return 2
    return 0

KEYWORDS = ["AI", "cloud", "cybersecurity", "stocks", "policy", "finance"]

def keyword_score(title):
    return sum(2 for kw in KEYWORDS if kw.lower() in title.lower())

def score_article(article, mention_count):
    return (
        SOURCE_WEIGHTS.get(article.domain, SOURCE_WEIGHTS["default"])
        + recency_score(article.published, now)
        + keyword_score(article.title)
        + mention_count * 2
    )