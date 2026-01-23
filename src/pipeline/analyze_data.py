import analysis_functions as af
import preprocessing_functions as pf
import data_utils as ut

def main():
    # Load in data
    clean_data = ut.load_comments("clean")
    raw_data = ut.load_comments("raw")
    stop_words = ut.load_stopwords()

    # Calculate uni, bi and trigram frequency for entire corpus : CLEAN DATA as input
    unigram_freq = {}
    for comments in clean_data.values():
        unigram_freq = af.calculate_word_frequency(comments, unigram_freq)
    bigrams, trigrams = af.find_ngrams(clean_data, 2), af.find_ngrams(clean_data, 3)

    # Sort unigram, count bi/trigrams
    unigram_freq = dict(sorted(unigram_freq.items(), key=lambda item: item[1]))
    bigram_freq, trigram_freq = af.count_ngrams(bigrams), af.count_ngrams(trigrams)

    # Post and corpus level analysis : RAW and CLEAN DATA as input
    post_analysis = af.analyze_posts(raw_data, clean_data)
    corpus_analysis = af.analyze_corpus(raw_data, clean_data)

    proj_root = ut.find_project_root()
    data_dir = proj_root / "src" / "data" / "clean"

    # Save analysis
    ut.save_data(post_analysis, "post_analysis.json", data_dir)
    ut.save_data(corpus_analysis, "corpus_analysis.json", data_dir)
    ut.save_data(unigram_freq, "unigram_freq.json", data_dir)
    ut.save_data(bigram_freq, "bigram_freq.json", data_dir)
    ut.save_data(trigram_freq, "trigram_freq.json", data_dir)

if __name__ == "__main__":
    main()
