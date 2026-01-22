import json
import preprocessing_functions as pf
from collections import Counter

# Count frequency of words
# Corpus or per post
def calculate_word_frequency(comments, word_freq):
    word_freq.update(Counter(comments))
    return word_freq

# Find n-grams from cleaned data
def find_ngrams(data, n):
    ngrams = []
    comments = data.values()
    # Go through comments of each post
    for v in comments:
        # Index to stop generating ngrams
        stop = len(v)-n+1
        for i in range(stop):
            # Append as tuple for counting
            ngrams.append(tuple(v[i:i+n]))
    return ngrams

# Count occurences of each ngram
def count_ngrams(ngrams):
    counts = Counter(ngrams)
    counts = dict(sorted(counts.items(), key=lambda item: item[1]))
    # Join ngram from tuple into string
    return {" ".join(ngram): count for ngram, count in counts.items()}

# Count comments for entire dataset
def get_comments_count(data):
    return sum(len(c) for c in data.values())

# Find statistics for posts
def analyse_posts(raw_data, clean_data):
    posts_analysis = {}

    for p, comments in raw_data.items():
        # Word freq for this post
        word_freq = {}

        # Number of comments for current post
        num_comments = len(comments)

        # Find total length of raw comments
        raw_length = sum(len(pf.tokenize(pf.clean(c))) for c in comments)

        # Find total length, unique words, word freq and top words of cleaned comments
        clean_length = len(clean_data[p])
        unique_words = set(clean_data[p])
        word_freq = calculate_word_frequency(clean_data[p], word_freq)
        top_words = [word for word, count in sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]]

        # All stats for this post
        post_stats = {"comment_count": num_comments, "avg_raw_length": raw_length/num_comments, "avg_clean_length": clean_length/num_comments, "unique_words": len(unique_words), "vocab_richness": len(unique_words)/clean_length, "top_words": top_words}

        posts_analysis[p] = post_stats

    return posts_analysis
