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

## Usage

**Create data directories and log file:**
```bash
mkdir ./src/data/
mkdir ./src/data/raw
mkdir ./src/data/clean
touch ./src/data/scrape_logs.json && echo {} >> scrape_logs.json
```

**Scrape a subreddit:**
```bash
python src/pipeline/get_data.py -s <subreddit> -f <from_hours> -u <until_hours> -l <limit> [-n|-h|-t|-c]
# Listing options: -n (new), -h (hot), -t (top), -c (controversial)
```

**Analyze scraped data:**
```bash
python src/pipeline/analyze_subreddit.py <subreddit>
python src/pipeline/generate_insights.py <subreddit>
```

**Batch processing:**
```bash
./scripts/scrape.sh     # Scrape multiple subreddits
./scripts/analyze.sh    # Analyze multiple subreddits
```

Results are saved to `src/data/clean/<subreddit>/`

---

## Status
**Completed:** Full NLP analysis pipeline with multi-subreddit support. Core features (preprocessing, TF-IDF, cosine similarity) implemented from scratch. Metadata tracking and batch processing scripts ready.

**Next:** Production hardening (error handling, logging, documentation, tests) and web UI development.

---

## License
MIT
