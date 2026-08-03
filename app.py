import os
import re
import requests
from difflib import SequenceMatcher
from flask import Flask, jsonify
from fetcher import fetch_all_feeds
from scoring import score_article

app = Flask(__name__)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
CHAT_IDS = [c.strip() for c in os.environ.get("TELEGRAM_CHAT_IDS", "").split(",") if c.strip()]
TOP_N = int(os.environ.get("TOP_N", 10))

def normalize_title(title):
    return re.sub(r'[^a-z0-9\s]', '', title.lower()).strip()

def compute_mention_counts(articles, threshold=0.7):
    normalized = [normalize_title(a["title"]) for a in articles]
    counts = [0] * len(articles)
    for i in range(len(articles)):
        for j in range(len(articles)):
            if i == j:
                continue
            similarity = SequenceMatcher(None, normalized[i], normalized[j]).ratio()
            if similarity >= threshold:
                counts[i] += 1
    return counts

def get_ranked_articles():
    articles = fetch_all_feeds()
    mention_counts = compute_mention_counts(articles)
    scored = [
        (article, score_article(article, mention_counts[i]))
        for i, article in enumerate(articles)
    ]
    scored.sort(key=lambda x: x[1], reverse=True)
    return [a for a, s in scored[:TOP_N]]

def send_digest(articles):
    if not BOT_TOKEN or not CHAT_IDS:
        return {"sent": False, "reason": "missing bot token or chat ids"}
    text = "\n\n".join(f"📰 {a['title']}\n{a['link']}" for a in articles)
    for chat_id in CHAT_IDS:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": chat_id, "text": text}
        )
    return {"sent": True, "chat_count": len(CHAT_IDS)}

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/headlines")
def headlines():
    try:
        return jsonify(get_ranked_articles())
    except Exception as e:
        import traceback
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

@app.route("/send-digest")
def send_digest_route():
    try:
        top = get_ranked_articles()
        result = send_digest(top)
        return jsonify({"status": "done", "count": len(top), **result})
    except Exception as e:
        import traceback
        return jsonify({"error": str(e), "trace": traceback.format_exc()}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)