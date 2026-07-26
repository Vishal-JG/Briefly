from flask import Flask, jsonify
from fetcher import fetch_all_feeds
from scoring import score_article

app = Flask(__name__)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/headlines")
def headlines():
    articles = fetch_all_feeds()
    ranked = sorted(articles, key=lambda a: score_article(a), reverse=True)
    return jsonify(ranked[:8])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)