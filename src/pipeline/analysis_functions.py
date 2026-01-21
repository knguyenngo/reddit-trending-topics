import json
import preprocessing_functions as pf
import scrape_functions as sf
from collections import Counter

# Calculate word frequency for entire dataset
def calculate_word_frequency(comments):
    word_freq = {}
    # Count word freq
    for c in comments.values():
        for word in c:
            if word in word_freq:
                word_freq[word] = word_freq[word] + 1
            else:
                word_freq[word] = 1
    # Return dict sorted by frequency
    return dict(sorted(word_freq.items(), key=lambda item: item[1]))

# Find n-grams from cleaned data
def find_ngrams(comments, n):
    ngrams = []
    values = comments.values()
    # Go through comments of each post
    for v in values:
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

# Save data to JSON
def save_data(data, file_name, data_dir):
    with open(f"{data_dir}/{file_name}", "w") as json_file:
        json.dump(data, json_file, indent=1)

# Count frequency of words per post
def post_word_frequency(comments):
    word_freq = {}
    for word in comments:
        if word in word_freq:
            word_freq[word] = word_freq[word] + 1
        else:
            word_freq[word] = 1
    return dict(sorted(word_freq.items(), key=lambda item: item[1]))

# Perform post level analysis and save data
def post_level_analysis(data, data_dir):
    for p, c in data.items():
        data[p] = post_word_frequency(c)
    save_data(data, "post_level_analysis.json", data_dir)

