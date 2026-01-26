import data_utils as ut
import similarity_functions as sm

def main():
    # Load in data
    unigram_freq = ut.load_analysis("unigram_freq.json")
    posts_tfidf = ut.load_analysis("tfidf_analysis.json")

    # Sort all unique words a-z
    word_types = sorted(unigram_freq.keys())
    all_post_vectors = {}

    # Get all post vectors
    for post, analysis in posts_tfidf.items():
        post_vector = sm.vectorize_posts(analysis["tfidf_scores"], word_types)
        all_post_vectors[post] = post_vector

    # Find similar posts for all posts
    similarity_analysis = {}
    for post in posts_tfidf.keys():
        similar_posts = sm.find_similar_posts(post, all_post_vectors)
        similarity_analysis[post] = similar_posts

    # Save data
    data_dir = ut.find_project_root() / "src" / "data" / "clean"
    ut.save_data(similarity_analysis, "similarity_analysis.json", data_dir)

if __name__ == "__main__":
    main()
