import math
import analysis_functions as af

def calculate_idf(clean_data):
    # Load in data
    total_posts = len(clean_data)

    # Find unique words
    unique_words = set().union(*clean_data.values())
    word_appearance, idf = {}, {}

    # Count appearance of word within posts
    for word in unique_words:
        word_appearance[word] = 0
        for comments in clean_data.values():
            if word in comments:
                word_appearance[word] += 1

    # Calculate IDF for each word
    for word in word_appearance.keys():
        idf[word] = math.log(total_posts / word_appearance[word])
    return idf

def calculate_tfidf(post_tokens, idf):
    word_freq, tfidf = {}, {}

    # Get word frequency within post
    word_freq = af.calculate_word_frequency(post_tokens, word_freq)
    total_tokens = len(post_tokens)

    # Calculate TFIDF
    for word in word_freq.keys():
        tf_value = word_freq[word] / total_tokens
        tf_idf_value = tf_value * idf[word]
        tfidf[word] = tf_idf_value

    return tfidf

def get_top_tfidf_words(tfidf, n=10):
    # Get top N words from tfidf values of post
    return [word for word, count in sorted(tfidf.items(), key=lambda x: x[1], reverse=True)[:n]]
