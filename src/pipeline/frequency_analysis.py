import json
import preprocessing_functions as pf
import scrape_functions as sf
from collections import Counter

# Calculate word frequency for dataset
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

def save_data(data, file_name, data_dir):
    with open(f"{data_dir}/{file_name}", "w") as json_file:
        json.dump(data, json_file, indent=1)

def main():
    # Load comments
    comments = pf.load_comments("clean")
    # Calculate unigram freq
    unigram_freq = calculate_word_frequency(comments)

    # Find bigrams and trigrams from unigram tokens
    bigrams = find_ngrams(comments, 2)
    trigrams = find_ngrams(comments, 3)

    # Calculate bigrams and trigrams freq
    bigram_freq = count_ngrams(bigrams)
    trigram_freq = count_ngrams(trigrams)

    # Dir to save data
    project_dir = sf.find_project_root()
    save_dir = project_dir / "src" / "data" / "clean"

    # Save to JSON
    save_data(unigram_freq, "unigram_frequency.json", save_dir)
    save_data(bigram_freq, "bigram_frequency.json", save_dir)
    save_data(trigram_freq, "trigram_frequency.json", save_dir)

if __name__ == "__main__":
    main()
