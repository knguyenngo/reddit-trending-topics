# Project Outline

## Purpose
The purpose of this project is to learn Data Engineering concepts by implementing a functional data pipeline with data visualization.

## Stack
1. Python - for implementing initial pipeline and glue of project
2. Spark - distributed data processing
3. Airflow - workflow scheduler
4. SQLite - for loading gold level data
5. Streamlit - data visualization

## Phase I

### Main Goal
The goal for this phase is to implement functional pipeline in Python

### Steps
1. Scrape main page JSON
2. From the main page JSON, scrape individual posts JSON
3. Gather metadata of posts (upvotes, comments)

### Potential Problems
1. Request limit
2. Nested comments
3. Deleted posts/comments
4. Constant update VS 24 HR snapshots

### To-Do
1. Flatten JSON of individual posts to gather comment data (DONE)
2. Gather all comments disregarding relations (DONE)
3. Attempt to scrape r/MMA (DONE)
4. Flatten entire post file to extract parent pposts of comments/ignore parent comments (DONE)
5. Get HuggingFace model working for post summarization (DONE)
6. Design algorithm for processing and extracting summaries/sentiment from posts -> Next Phase

## Conclusion
Basic scraping functional, not a full pipeline but viable for MVP

## Phase II

### Main Goal
Design text analysis algorithm to extract big ideas from Subreddit from specific time range then implement a prototype

### To-Do
1. Explore NLP Concepts/Methods

## Conclusion
Stick to Topic Modeling for MVP

## Phase III

### Main Goal
Create MVP by visualizing scraped data: React/TS Vite App

### To-Do
1. Continue with design on Figma (CRAPPY)
2. Figure out components: Comments, Topic Bubbles, Posts (DONE BUT NEED REFINEMENT)
3. Restructure data for visualization in React App (DONE, JSON now has all posts for each TOPIC)
4. Continue working on visualizations and refining components (DONE, GOOD ENOUGH MOCKUP)

## Phase IV

### Main Goal
The goal of this phase is to move from basic Python to Spark for data processing

### To-Do
1. First change to REDDIT PRAW to fix Reddit limit issue (DONE)
2. Need to change scrape logic to ensure quality data for DS task (DONE)
3. Finished Airflow orchestration (DONE)
4. Figure out how to keep Airflow running to run schedule tasks (WORKING): Potentially use Oracle, for now run locally and maybe figure out how to start airflow at specific time to run DAG
