import re
from difflib import SequenceMatcher

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