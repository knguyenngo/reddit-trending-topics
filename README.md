# Reddit Theme Explorer

## What this is

This project pulls posts and comments from a subreddit, organizes conversations into high-level themes, and presents them in a simple UI so it’s easier to see what people are actually talking about.

Data is collected in snapshots, so each run captures a moment in time rather than trying to mirror Reddit live.

---

## Why it’s useful

Large Reddit threads are hard to read once they grow. This app focuses on making conversations easier to explore by organizing discussion at the theme level and surfacing representative posts and comments.

---

## What it does
- Collects Reddit posts and comments
- Handles nested threads and deleted content
- Uses open-source machine learning models to summarize and group discussions
- Groups conversations into themes
- Shows top posts and comments per theme
- Visualizes everything in a web app

---

## Tech stack
- **Python** – data collection and processing  
- **Hugging Face** – open-source NLP models for summarization and theme extraction  
- **Apache Spark** – scalable text processing  
- **Apache Airflow** – scheduled pipelines  
- **SQLite** – storing processed results  
- **React + TypeScript (Vite)** – interactive frontend  

---

## Status

Actively evolving. Core data flow, analysis, and UI are in place, with room to refine models, visuals, and automation.

---

## License

MIT License © 2026 Khuong Nguyen
