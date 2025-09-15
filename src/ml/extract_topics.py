import json
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np

POST = "../data/clean/all_posts.json"

def clean_posts(posts):
    """Clean and filter posts to remove junk"""
    cleaned = []
    
    for post in posts:
        # Skip deleted/removed content
        if post in ['[deleted]', '[removed]'] or post.strip() in ['[deleted]', '[removed]']:
            continue
            
        # Skip very short posts (likely low quality)
        if len(post.strip()) < 50:
            continue
            
        # Skip posts that are mostly repetition
        words = post.split()
        if len(set(words)) < len(words) * 0.3:  # Less than 30% unique words
            continue
            
        # Basic cleaning
        cleaned_post = re.sub(r'http\S+|www\S+', '', post)  # Remove URLs
        cleaned_post = re.sub(r'[^\w\s]', ' ', cleaned_post)  # Remove special chars
        cleaned_post = re.sub(r'\s+', ' ', cleaned_post).strip()  # Normalize whitespace
        
        if len(cleaned_post) > 30:  # Final length check
            cleaned.append(cleaned_post)
    
    return cleaned

def simple_topic_modeling(posts, n_topics=10):
    """Simple topic modeling using LDA"""
    
    # Vectorize the text
    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words='english',
        min_df=5,  # Word must appear in at least 5 documents
        max_df=0.7,  # Word can't appear in more than 70% of documents
        ngram_range=(1, 2)  # Include bigrams
    )
    
    doc_term_matrix = vectorizer.fit_transform(posts)
    
    # LDA Topic Modeling
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        max_iter=10
    )
    
    lda.fit(doc_term_matrix)
    
    # Get topic assignments for each post
    topic_assignments = lda.transform(doc_term_matrix).argmax(axis=1)
    
    # Get top words for each topic
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    
    for topic_idx, topic in enumerate(lda.components_):
        top_words_idx = topic.argsort()[-10:][::-1]  # Top 10 words
        top_words = [feature_names[i] for i in top_words_idx]
        topics.append({
            'id': topic_idx,
            'words': top_words,
            'posts': []
        })
    
    # Group posts by topic
    for i, topic_id in enumerate(topic_assignments):
        topics[topic_id]['posts'].append(posts[i])
    
    return topics

def create_topic_summaries(topics):
    """Create simple summaries for each topic"""
    summaries = []
    
    for topic in topics:
        if len(topic['posts']) < 3:  # Skip topics with too few posts
            continue
            
        # Simple summary: top words + post count
        word_summary = " | ".join(topic['words'][:5])
        
        # Sample a few posts for context
        sample_posts = topic['posts'][:3] if len(topic['posts']) >= 3 else topic['posts']
        sample_text = " ... ".join([post[:100] for post in sample_posts])
        
        summaries.append({
            'topic_id': topic['id'],
            'keywords': word_summary,
            'post_count': len(topic['posts']),
            'sample_content': sample_text,
            'top_words': topic['words'][:10],
            'posts' : topic['posts']
        })
    
    # Sort by post count (largest topics first)
    summaries.sort(key=lambda x: x['post_count'], reverse=True)
    return summaries

def main():
    # Load data
    with open(POST, "r") as json_file:
        post_data = json.load(json_file)
    
    print(f"Loaded {len(post_data)} posts")
    
    # Clean posts
    cleaned_posts = clean_posts(post_data)
    print(f"After cleaning: {len(cleaned_posts)} posts ({len(cleaned_posts)/len(post_data)*100:.1f}% retained)")
    
    if len(cleaned_posts) < 50:
        print("Not enough clean posts for topic modeling!")
        return
    
    # Simple topic modeling
    n_topics = min(10, len(cleaned_posts) // 20)  # Adaptive number of topics
    print(f"Creating {n_topics} topics...")
    
    topics = simple_topic_modeling(cleaned_posts, n_topics)
    
    # Create summaries
    summaries = create_topic_summaries(topics)
    
    # Print results
    print(f"\n=== TOPIC MODELING RESULTS ===")
    print(f"Found {len(summaries)} meaningful topics from {len(cleaned_posts)} posts\n")
    
    #for i, summary in enumerate(summaries, 1):
    #    print(f"Topic {i} ({summary['post_count']} posts)")
    #    print(f"Keywords: {summary['keywords']}")
    #    print(f"Sample: {summary['sample_content'][:200]}...")
    #    print("-" * 80)
    with open("../data/clean/topics.json", "w") as json_file:
        json.dump(summaries, json_file, indent=1)

if __name__ == "__main__":
    main()
