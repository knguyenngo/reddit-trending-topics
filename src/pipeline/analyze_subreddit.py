# Data handling
import data_utils as ut

# Text processing
import preprocessing_functions as pf

# Analysis modules
import analysis_functions as af
import tfidf_functions as tf
import similarity_functions as sm

def main():
    # ============================================================================
    # STEP 1: LOAD RAW DATA
    # ============================================================================
    raw_data = ut.load_comments("raw")
    stopwords = ut.load_stopwords()
    clean_data = {}
    posts_tfidf = {}
    
    # ============================================================================
    # STEP 2: PREPROCESS - Clean and tokenize all comments
    # ============================================================================
    # Clean raw comments into a list of individual tokens
    for post, comments in raw_data.items():
        cleaned_comments = []
        for comment in comments:
            cleaned_comments.extend(pf.preprocess_comment(comment, stopwords))
        clean_data[post] = cleaned_comments
    
    # ============================================================================
    # STEP 3: FREQUENCY ANALYSIS - Calculate n-gram frequencies
    # ============================================================================
    # Calculate unigram frequency for entire corpus
    unigram_freq = {}
    for comments in clean_data.values():
        unigram_freq = af.calculate_word_frequency(comments, unigram_freq)
    
    # Calculate bigrams and trigrams
    bigrams, trigrams = af.find_ngrams(clean_data, 2), af.find_ngrams(clean_data, 3)
    
    # Sort unigram by frequency, count bi/trigrams
    unigram_freq = dict(sorted(unigram_freq.items(), key=lambda item: item[1]))
    bigram_freq, trigram_freq = af.count_ngrams(bigrams), af.count_ngrams(trigrams)
    
    # ============================================================================
    # STEP 4: STATISTICAL ANALYSIS - Post and corpus level metrics
    # ============================================================================
    post_analysis = af.analyze_posts(raw_data, clean_data)
    corpus_analysis = af.analyze_corpus(raw_data, clean_data)
    
    # ============================================================================
    # STEP 5: TF-IDF - Calculate term importance
    # ============================================================================
    # Calculate IDF scores across corpus
    idf = tf.calculate_idf(clean_data)
    
    # Calculate TF-IDF for each post and extract top words
    for post, tokens in clean_data.items():
        post_tfidf = tf.calculate_tfidf(tokens, idf)
        top_words = tf.get_top_tfidf_words(post_tfidf)
        posts_tfidf[post] = {"top_tfidf_words" : top_words, "tfidf_scores" : post_tfidf}
    
    # ============================================================================
    # STEP 6: VECTORIZATION - Convert TF-IDF to vectors
    # ============================================================================
    # Create consistent vocabulary ordering (sorted a-z)
    word_types = sorted(unigram_freq.keys())
    all_post_vectors = {}
    
    # Vectorize all posts using TF-IDF scores
    for post, analysis in posts_tfidf.items():
        post_vector = sm.vectorize_posts(analysis["tfidf_scores"], word_types)
        all_post_vectors[post] = post_vector
    
    # ============================================================================
    # STEP 7: SIMILARITY ANALYSIS - Find related posts
    # ============================================================================
    similarity_analysis = {}
    for post in posts_tfidf.keys():
        similar_posts = sm.find_similar_posts(post, all_post_vectors)
        similarity_analysis[post] = similar_posts
    
    # ============================================================================
    # STEP 8: SAVE RESULTS
    # ============================================================================
    data_dir = ut.find_project_root() / "src" / "data" / "clean"
    ut.save_data(similarity_analysis, "similarity_analysis.json", data_dir)
    ut.save_data(posts_tfidf, "tfidf_analysis.json", data_dir)
    ut.save_data(post_analysis, "post_analysis.json", data_dir)
    ut.save_data(corpus_analysis, "corpus_analysis.json", data_dir)
    ut.save_data(unigram_freq, "unigram_freq.json", data_dir)
    ut.save_data(bigram_freq, "bigram_freq.json", data_dir)
    ut.save_data(trigram_freq, "trigram_freq.json", data_dir)

if __name__ == "__main__":
    main()
