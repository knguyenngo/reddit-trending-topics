import data_utils as ut
import sys

def main():
    # ============================================================================
    # STEP 0: GET SUBREDDIT FROM COMMAND LINE
    # ============================================================================
    if len(sys.argv) < 2:
        print("Error: Subreddit name required")
        print("Usage: python generate_insights.py <subreddit_name>")
        sys.exit(1)
    
    subreddit = sys.argv[1]
    print(f"Generating insights for r/{subreddit}...")
    
    # ============================================================================
    # STEP 1: LOAD ANALYSIS DATA
    # ============================================================================
    data_dir = ut.find_project_root() / "src" / "data" / "clean" / subreddit
    
    corpus_analysis = ut.load_data("corpus_analysis.json", data_dir)
    posts_analysis = ut.load_data("post_analysis.json", data_dir)
    tfidf_analysis = ut.load_data("tfidf_analysis.json", data_dir)
    similar_posts = ut.load_data("similarity_analysis.json", data_dir)
    unigram_freq = ut.load_data("unigram_freq.json", data_dir)
    bigram_freq = ut.load_data("bigram_freq.json", data_dir)
    trigram_freq = ut.load_data("trigram_freq.json", data_dir)
    
    # ============================================================================
    # STEP 2: EXTRACT TOP N-GRAMS
    # ============================================================================
    corpus_analysis["top_unigrams"] = list(unigram_freq.keys())[-20:]
    corpus_analysis["top_bigrams"] = list(bigram_freq.keys())[-20:]
    corpus_analysis["top_trigrams"] = list(trigram_freq.keys())[-15:]
    
    # ============================================================================
    # STEP 3: EXTRACT HIGHEST ENGAGEMENT POSTS
    # ============================================================================
    posts_analysis = dict(sorted(posts_analysis.items(), key=lambda item: item[1]['comment_count'], reverse=True))
    corpus_analysis["top_engaged_posts"] = dict(list(posts_analysis.items())[:20])
    
    # ============================================================================
    # STEP 4: EXTRACT TOPIC CLUSTERS
    # ============================================================================
    top_posts = corpus_analysis["top_engaged_posts"]
    topic_clusters = {}
    for post_id in top_posts:
        post_data = top_posts[post_id]
        similar_posts_to_id = similar_posts[post_id]

        # Go through similar posts and add top tfidf for each post
        for similar in similar_posts_to_id:
            similar_id = similar["post_id"]
            top_words = tfidf_analysis[similar_id]["top_tfidf_words"]
            similar["top_words"] = top_words

        topic_clusters[post_data["title"]] = similar_posts[post_id]
    corpus_analysis["topic_clusters"] = topic_clusters
    
    # ============================================================================
    # STEP 5: EXTRACT DISTINCT POSTS
    # ============================================================================
    posts_analysis = dict(sorted(posts_analysis.items(), key=lambda item: item[1]['vocab_richness'], reverse=True))
    corpus_analysis["distinct_posts"] = dict(list(posts_analysis.items())[:20])
    
    # ============================================================================
    # STEP 6: SAVE INSIGHTS
    # ============================================================================
    ut.save_data(corpus_analysis, "final_insights.json", data_dir)
    print(f"Insights generated! Saved to {data_dir}/final_insights.json")

if __name__ == "__main__":
    main()
