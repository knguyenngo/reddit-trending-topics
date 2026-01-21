import analysis_functions as af
import preprocessing_functions as pf
import scrape_functions as sf

def main():
    # Load comments
    comments = pf.load_comments("clean")
    # Calculate unigram freq
    unigram_freq = af.calculate_word_frequency(comments)

    # Find bigrams and trigrams from unigram tokens
    bigrams = af.find_ngrams(comments, 2)
    trigrams = af.find_ngrams(comments, 3)

    # Calculate bigrams and trigrams freq
    bigram_freq = af.count_ngrams(bigrams)
    trigram_freq = af.count_ngrams(trigrams)

    # Dir to save data
    project_dir = sf.find_project_root()
    save_dir = project_dir / "src" / "data" / "clean"

    # Calculate ost level analysis and save
    af.post_level_analysis(comments, save_dir)

    # Save to JSON
    af.save_data(unigram_freq, "unigram_frequency.json", save_dir)
    af.save_data(bigram_freq, "bigram_frequency.json", save_dir)
    af.save_data(trigram_freq, "trigram_frequency.json", save_dir)

if __name__ == "__main__":
    main()
