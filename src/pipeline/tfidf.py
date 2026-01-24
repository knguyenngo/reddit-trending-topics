import tfidf_functions as tf
import data_utils as ut

def main():
    clean_data = ut.load_comments("clean")
    tfidf_analysis = {}

    # Calculate IDF
    idf = tf.calculate_idf(clean_data)
    
    # Calculate tfidf for each post and top tfidf words for each post
    for post, tokens in clean_data.items():
        post_tfidf = tf.calculate_tfidf(tokens, idf)
        top_words = tf.get_top_tfidf_words(post_tfidf)
        # Add data to dict
        tfidf_analysis[post] = {"top_tfidf_words" : top_words, "tfidf_scores" : post_tfidf}

    # Save JSON
    data_dir = ut.find_project_root() / "src" / "data" / "clean"
    ut.save_data(tfidf_analysis, "tfidf_analysis.json", data_dir) 

if __name__ == "__main__":
    main()
