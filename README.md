# Briefly

A self-hosted news aggregation bot that fetches, ranks, and delivers the most 
important tech and political headlines from the US, Singapore, India, and 
Australia — built as a personal homelab project to learn Kubernetes, DevOps 
practices, and self-hosted infrastructure hands-on.

This started as a learning exercise: rather than reading Kubernetes docs in 
isolation, I built a real app (Briefly) and used it as the vehicle to learn 
container orchestration, secure remote access, and CI/CD — the same stack 
used in production DevOps environments, just running on a single repurposed 
Lenovo AIO at home.

## Why This Exists

I wanted to stop mindlessly scrolling news apps every morning and instead get 
a short, ranked digest of what actually matters — without relying on an LLM 
or a paid news API. Briefly uses a transparent, explainable scoring heuristic 
instead of machine learning, which was a deliberate choice: it's simpler to 
build, debug, and explain than an ML pipeline, while still surfacing genuinely 
important stories.

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.12 |
| Web framework | Flask |
| RSS parsing | feedparser |
| Containerization | Docker |
| Orchestration | k3s (lightweight Kubernetes) |
| Networking | Tailscale + Tailscale Kubernetes Operator |
| Registry | GitHub Container Registry (GHCR) |
| CI/CD | GitHub Actions |
| Notifications | Telegram Bot API |

## How the Ranking Works

No LLM or ML model is used. Headlines are scored using a weighted heuristic:

- **Source authority** — known outlets (Reuters, AP, BBC) score higher than 
  smaller sources
- **Recency** — articles published in the last 6-12 hours are weighted heavier
- **Keyword relevance** — headlines matching topics like AI, cloud, elections, 
  and policy get a small boost
- **Cross-source corroboration** — if 3+ sources report a similar story 
  (detected via fuzzy title matching), that's treated as a strong signal of 
  importance and boosted further

