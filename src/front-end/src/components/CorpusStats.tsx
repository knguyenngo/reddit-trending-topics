import React from "react";
import type { CorpusAnalysis } from "../types/index.ts"

function CorpusStats(props: { data : CorpusAnalysis}) {
  return (
    <div class="mx-auto flex items-center text-2xl font-small">
      <p>Total Comments: {props.data.total_comments}</p>
      <p>Total Tokens: {props.data.total_tokens}</p>
      <p>Vocabulary Size: {props.data.vocabulary_size}</p>
      <p>Vocabulary Richness: {props.data.vocabulary_richness}</p>
      <p>Top Unigrams: {props.data.top_unigrams.join(', ')}</p>
    </div>
  );
}

export default CorpusStats;
