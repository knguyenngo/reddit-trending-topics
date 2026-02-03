import React from "react";
import type { CorpusAnalysis } from "../types/index.ts"

function CorpusStats(props: { data : CorpusAnalysis}) {
  return (
    <div className="bg-red-500 rounded-[2rem] grid grid-cols-2 grid-rows-2 gap-4 w-full h-full p-4">
      {/* Card 1 */}
      <div className="bg-white rounded-[2rem] flex flex-col items-center justify-center p-6 shadow-sm">
        <span className="text-gray-500 text-sm font-medium">Total Comments</span>
        <span className="text-3xl font-bold text-black">{props.data.total_comments}</span>
      </div>

      {/* Card 2 */}
      <div className="bg-white rounded-[2rem] flex flex-col items-center justify-center p-6 shadow-sm">
        <span className="text-gray-500 text-sm font-medium">Total Tokens</span>
        <span className="text-3xl font-bold text-black">{props.data.total_tokens}</span>
      </div>

      {/* Card 3 */}
      <div className="bg-white rounded-[2rem] flex flex-col items-center justify-center p-6 shadow-sm">
        <span className="text-gray-500 text-sm font-medium">Vocabulary Size</span>
        <span className="text-3xl font-bold text-black">{props.data.vocabulary_size}</span>
      </div>

      {/* Card 4 */}
      <div className="bg-white rounded-[2rem] flex flex-col items-center justify-center p-6 shadow-sm">
        <span className="text-gray-500 text-sm font-medium">Vocabulary Richness</span>
        <span className="text-3xl font-bold text-black truncate w-full text-center">
          {props.data.vocabulary_richness.toFixed(4)*100}
        </span>
      </div>
    </div>
  );
}

export default CorpusStats;
