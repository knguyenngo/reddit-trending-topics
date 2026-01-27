# Reddit Theme Explorer

## What this is
This project pulls posts and comments from a subreddit and analyzes discussion patterns using natural language processing. It identifies key themes, distinctive vocabulary, and conversation clusters to help you understand what a community is actually talking about.

Data is collected in snapshots, so each run captures a moment in time rather than trying to mirror Reddit live.

---

## Why it's useful
Large subreddits generate thousands of comments that are hard to parse. This tool focuses on making conversations easier to explore by:
- Identifying the most discussed topics (n-grams)
- Finding what makes each post unique (TF-IDF)
- Clustering similar discussions together
- Highlighting distinctive vs common vocabulary

---

## What it does
- Scrapes Reddit posts and comments using PRAW
- Cleans and tokenizes text (removes noise, stopwords, Reddit formatting)
- Calculates word frequencies and n-grams (bigrams, trigrams)
- Computes TF-IDF scores to identify important terms per post
- Uses cosine similarity to find related discussions
- Generates comprehensive analysis reports with:
  - Corpus-level statistics (vocabulary size, engagement metrics)
  - Top engaged posts and their themes
  - Topic clusters based on similarity
  - Posts with distinctive vocabulary

---

## Status
Analysis pipeline complete. Core NLP features implemented from scratch (preprocessing, TF-IDF, cosine similarity). Currently working on metadata tracking and multi-subreddit support.

---

## License
MIT
