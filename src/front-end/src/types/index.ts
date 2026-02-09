interface CorpusAnalysis {
  total_comments: number;
  total_tokens: number;
  vocabulary_size: number;
  vocabulary_richness: number;
  top_unigrams: string[];
  top_bigrams: string[];
  top_trigrams: string[];
  top_engaged_posts: Record<string, PostAnalysis>;
}

interface PostAnalysis {
  title: string;
  time_created: number;
  comment_count: number;
  avg_raw_length: number;
  avg_clean_length: number;
  unique_words: number;
  vocab_richness: number;
  top_words: string[];
}

interface TFIDFAnalysis {
  top_tfidf_words: string[];
  tfidf_scores: Record<string, number>;
}

type SimilarityAnalysis = Record<string, [string, number][]>;

type UnigramFrequency = Record<string, number>;
