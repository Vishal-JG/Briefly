from flask import Flask, jsonify
from fetcher import fetch_all_feeds
from scoring import score_article
from dedupe import compute_mention_counts

app = Flask(__name__)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/headlines")
def headlines():
    articles = fetch_all_feeds()
    mention_counts = compute_mention_counts(articles)
    scored = [(a, score_article(a, mention_counts[i])) for i, a in enumerate(articles)]
    scored.sort(key=lambda x: x[1], reverse=True)
    return jsonify([a for a, s in scored[:8]])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)