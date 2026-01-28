import data_utils as ut

def main():
    data_dir = find_project_root() / "src" / "data" / "clean"

    corpus_analysis = ut.load_data("corpus_analysis.json", data_dir)
    posts_analysis = ut.load_data("post_analysis.json", data_dir)
    tfidf_analysis = ut.load_data("tfidf_analysis.json", data_dir)
    similar_posts = ut.load_data("similarity_analysis.json", data_dir)
    unigram_freq = ut.load_data("unigram_freq.json", data_dir)
    bigram_freq = ut.load_data("bigram_freq.json", data_dir)
    trigram_freq = ut.load_data("trigram_freq.json", data_dir)

    # Extract top uni/bi/trigrams for entire dataset
    corpus_analysis["top_unigrams"] = list(unigram_freq.keys())[-20:]
    corpus_analysis["top_bigrams"] = list(bigram_freq.keys())[-20:]
    corpus_analysis["top_trigrams"] = list(trigram_freq.keys())[-15:]

    # Extract highest engagement posts
    posts_analysis = dict(sorted(posts_analysis.items(), key=lambda item: item[1]['comment_count'], reverse=True))
    corpus_analysis["top_engaged_posts"] = dict(list(posts_analysis.items())[:20])

    # Extract topic clusters from similar posts to top engagement posts
    top_posts = corpus_analysis["top_engaged_posts"]
    topic_clusters = {}
    for post in top_posts:
        topic_clusters[post] = similar_posts[post]
    corpus_analysis["topic_clusters"] = topic_clusters

    # Distinct posts with high vocab richness
    posts_analysis = dict(sorted(posts_analysis.items(), key=lambda item: item[1]['vocab_richness'], reverse=True))
    corpus_analysis["distinct_posts"] = dict(list(posts_analysis.items())[:20])

    # Save analysis
    data_dir = ut.find_project_root() / "src" / "data" / "clean"
    ut.save_data(corpus_analysis, "updated_corpus_analysis.json", data_dir) 

if __name__ == "__main__":
    main()
