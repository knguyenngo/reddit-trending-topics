// Generic function for fetch data from JSON
function fetchJSON<T>(subreddit: string, fileName: string): Promise<T> {
  return fetch(`/data/${subreddit}/${fileName}.json`)
    .then(response => {
      if (!response.ok) {
        throw new Error(`HTTP Error, Status: ${response.status}`);
      }
      return response.json();
    })
    .then(data => data as T)
}

// Grab analysis for individual posts
export const fetchPostAnalysis = (subreddit:string): Promise<Record<string, PostAnalysis>> => {
  return fetchJSON<Record<string, PostAnalysis>>(subreddit, "post_analysis");
}

// Grab analysis for entire dataset
export const fetchCorpusAnalysis = (subreddit: string): Promise<CorpusAnalysis> => {
  return fetchJSON<CorpusAnalysis>(subreddit, "final_insights");
}

// Grab TFIDF analysis for individual posts
export const fetchTFIDFAnalysis = (subreddit: string): Promise<TFIDFAnalysis> => {
  return fetchJSON<TFIDFAnalysis>(subreddit, "tfidf_analysis");
}

// Grab similarity analysis for individual posts
export const fetchSimilarityAnalysis = (subreddit: string): Promise<Record<string, SimilarityAnalysis>> => {
  return fetchJSON<Record<string, SimilarityAnalysis>>(subreddit, "similarity_analysis");
}

// Grab unigram frequencies for entire dataset
export const fetchUnigrams = (subreddit: string): Promise<UnigramFrequency> => {
  return fetchJSON<UnigramFrequency>(subreddit, "unigram_freq");
}
